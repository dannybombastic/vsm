"""
AI-powered Value Stream Map generator.

Collects questionnaire responses for a project, builds a structured prompt,
calls an LLM (OpenAI or Azure OpenAI), and returns a ValueStream definition
that can be persisted to the database.

AI configuration is read from the AIConfiguration singleton in the DB
(editable from Django Admin).
"""
import json
import logging
import re

from django.utils.text import slugify

from vsm.models import AIConfiguration, Category, FormResponse, Project

logger = logging.getLogger(__name__)

# ── Prompt templates ────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a Lean/Six-Sigma Value Stream Mapping expert. Your task is to analyze
questionnaire responses from multiple teams in a software delivery organization
and produce a complete Value Stream Map (VSM) as structured JSON.

A Value Stream Map shows the end-to-end flow of work from request to delivery,
with timing metrics for each process step.

RULES:
1. Identify the main process steps from the team responses (process descriptions,
   handoffs, bottlenecks, and quantitative metrics).
2. Order the steps in the logical flow of work (upstream → downstream).
3. Use TWO rows: row 0 for the primary flow, row 1 for secondary/parallel flows.
4. Map each step to the appropriate team category using its slug.
5. Extract realistic timing from the quantitative answers (section G metrics and
   section B tables). When specific numbers aren't available, estimate
   conservatively based on the qualitative descriptions.
6. Identify rework loops from pain points and waste descriptions.
7. The "analysis" field must contain your reasoning: why you chose these steps,
   how you estimated timings, key insights about waste and bottlenecks.

OUTPUT FORMAT (strict JSON, no markdown fences):
{{
  "name": "Value stream name",
  "description": "Brief description of this value stream",
  "steps": [
    {{
      "name": "Step name (concise, 3-6 words)",
      "category_slug": "one of the available slugs",
      "order": 1,
      "row": 0,
      "work_time": 8.0,
      "wait_time": 4.0,
      "loop_factor": 0.2,
      "loop_work_extra": 3.0,
      "num_people": 2,
      "flow_type": "push",
      "description": "Brief step description"
    }}
  ],
  "analysis": "Your detailed analysis and reasoning..."
}}

FIELD DEFINITIONS:
- work_time: Active process/touch time in hours (when people are actually working)
- wait_time: Idle/queue time before this step begins, in hours
- loop_factor: Probability of rework (0.0 = never, 1.0 = always). E.g. 0.3 = 30% rework
- loop_work_extra: Additional hours of work per rework iteration
- num_people: Number of people typically involved in this step
- flow_type: "push" (work is assigned) or "pull" (team picks from queue)
- row: 0 for main flow, 1 for secondary/parallel flow

AVAILABLE CATEGORY SLUGS:
{category_slugs}
"""

USER_PROMPT = """\
PROJECT: {project_name}
{project_description}

Below are the questionnaire responses from all teams, organized by category.
Analyze them and generate a complete Value Stream Map.

{responses_text}

Generate the VSM JSON now. Remember: output ONLY valid JSON, no markdown fences.
"""


# ── Response collector ──────────────────────────────────────────


def collect_responses_for_prompt(project: Project) -> tuple[str, list[int]]:
    """Gather all form responses for a project and format them for the prompt.

    Returns (formatted_text, list_of_response_ids).
    """
    categories = Category.objects.prefetch_related("sections__questions").order_by("order")
    responses = FormResponse.objects.filter(project=project).select_related("category")

    # Group responses by category
    by_category: dict[str, list[FormResponse]] = {}
    for resp in responses:
        by_category.setdefault(resp.category.slug, []).append(resp)

    lines = []
    response_ids = []

    for cat in categories:
        cat_responses = by_category.get(cat.slug, [])
        if not cat_responses:
            continue

        lines.append(f"\n{'='*60}")
        lines.append(f"TEAM/CATEGORY: {cat.name} (slug: {cat.slug})")
        lines.append(f"{'='*60}")

        for i, resp in enumerate(cat_responses, 1):
            response_ids.append(resp.pk)
            lines.append(f"\n--- Respondent {i}: {resp.respondent_name} ({resp.respondent_role}) ---")

            # Get questions for label lookup
            questions = {
                q.key: q
                for sec in cat.sections.all()
                for q in sec.questions.all()
            }

            for key, value in resp.data.items():
                q = questions.get(key)
                label = q.label if q else key
                section_code = q.section.code if q else "?"

                if isinstance(value, list):
                    if value and isinstance(value[0], dict):
                        # Table data
                        lines.append(f"  [{section_code}] {label}:")
                        for row in value:
                            row_str = " | ".join(f"{k}: {v}" for k, v in row.items())
                            lines.append(f"    - {row_str}")
                    else:
                        # Checklist
                        lines.append(f"  [{section_code}] {label}: {', '.join(str(v) for v in value)}")
                else:
                    lines.append(f"  [{section_code}] {label}: {value}")

    return "\n".join(lines), response_ids


# ── LLM client ──────────────────────────────────────────────────


def _get_openai_client():
    """Create an OpenAI client from the AIConfiguration singleton in the DB."""
    try:
        import openai
    except ImportError:
        raise RuntimeError(
            "The 'openai' package is required for AI VSM generation. "
            "Install it with: pip install openai"
        )

    config = AIConfiguration.load()
    if not config or not config.is_active or not config.api_key:
        raise RuntimeError(
            "La IA no está configurada. Ve a Admin → AI Configuration "
            "para introducir tu API key y endpoint."
        )

    if config.provider == "azure":
        if not config.endpoint:
            raise RuntimeError(
                "Azure OpenAI requiere un endpoint. "
                "Configúralo en Admin → AI Configuration."
            )
        return openai.AzureOpenAI(
            azure_endpoint=config.endpoint,
            api_key=config.api_key,
            api_version=config.api_version or "2024-06-01",
        ), config.model_name or "gpt-4o"

    # Standard OpenAI
    base_url = config.endpoint or None
    return openai.OpenAI(api_key=config.api_key, base_url=base_url), config.model_name or "gpt-4o"


def _get_ai_config():
    """Return the active AIConfiguration or None."""
    config = AIConfiguration.load()
    if config and config.is_active:
        return config
    return None


def _parse_json_response(text: str) -> dict:
    """Parse JSON from LLM response, handling markdown fences if present."""
    text = text.strip()
    # Strip markdown code fences
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


# ── Main generator ──────────────────────────────────────────────


def generate_vsm(project: Project) -> dict:
    """Generate a VSM from project questionnaire responses using AI.

    Returns a dict with keys: name, description, steps, analysis, response_ids.
    Raises RuntimeError if AI is not configured or call fails.
    """
    responses_text, response_ids = collect_responses_for_prompt(project)

    if not response_ids:
        raise ValueError(
            f"No hay respuestas de cuestionarios para el proyecto '{project.name}'. "
            "Los equipos deben rellenar los cuestionarios primero."
        )

    # Build prompts
    categories = Category.objects.all()
    category_slugs = "\n".join(
        f"  - {c.slug} ({c.name})" for c in categories
    )

    system_msg = SYSTEM_PROMPT.format(category_slugs=category_slugs)
    user_msg = USER_PROMPT.format(
        project_name=project.name,
        project_description=project.description or "(no description)",
        responses_text=responses_text,
    )

    # Call LLM
    client, model = _get_openai_client()
    config = _get_ai_config()

    logger.info("Calling LLM for VSM generation (project=%s, model=%s, responses=%d)",
                project.slug, model, len(response_ids))

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=config.temperature if config else 0.3,
        max_tokens=config.max_tokens if config else 4000,
    )

    raw_response = completion.choices[0].message.content
    logger.info("LLM response received (%d chars)", len(raw_response))

    # Parse
    result = _parse_json_response(raw_response)

    # Validate structure
    if "steps" not in result or not isinstance(result["steps"], list):
        raise ValueError("La respuesta de la IA no contiene pasos válidos.")

    # Validate category slugs
    valid_slugs = set(Category.objects.values_list("slug", flat=True))
    for step in result["steps"]:
        if step.get("category_slug") not in valid_slugs:
            step["category_slug"] = None

    # Generate slug for the VSM
    base_slug = slugify(result.get("name", f"{project.name} AI VSM"))
    result["slug"] = base_slug
    result["response_ids"] = response_ids
    result["generation_method"] = "ai"

    return result


def ai_is_configured() -> bool:
    """Check if AI is configured via the AIConfiguration singleton in the DB."""
    config = AIConfiguration.load()
    return bool(config and config.is_active and config.api_key)


# ── Suggestion prompts ──────────────────────────────────────────

SUGGESTIONS_SYSTEM_PROMPT = """\
You are a Lean/Six-Sigma Value Stream Mapping expert. You will receive the
results of a Value Stream Map (VSM) and must produce actionable improvement
suggestions.

Analyze the VSM data and provide suggestions organized in these sections:

1. **Cuellos de botella identificados**: Steps with the highest total time or
   wait time that constrain throughput.
2. **Reducción de tiempos de espera**: Specific wait times that can be reduced
   and how (automation, parallelization, pull systems).
3. **Eliminación de retrabajo**: Steps with loop_factor > 0 and concrete
   actions to reduce rework (better specs, earlier testing, code reviews).
4. **Optimización del flujo**: Opportunities to change push → pull, reduce
   handoffs, or consolidate steps.
5. **Quick wins**: Improvements achievable in 1-2 sprints with high impact.
6. **Mejoras a largo plazo**: Strategic changes requiring more effort but with
   significant Lead Time reduction.

For each suggestion, reference the specific step name and provide quantitative
impact estimates when possible (e.g. "reducing wait time from 8h to 2h would
save 6h per cycle").

Write in Spanish. Be specific and actionable — avoid generic advice.
"""

SUGGESTIONS_USER_PROMPT = """\
PROJECT: {project_name}

VALUE STREAM MAP: {vsm_name}
{vsm_description}

METRICS SUMMARY:
- Lead Time total: {lead_time:.1f}h
- Trabajo activo total: {total_work:.1f}h ({work_pct:.1f}%)
- Tiempo de bucles total: {total_loop:.1f}h ({loop_pct:.1f}%)
- Tiempo de espera total: {total_wait:.1f}h ({wait_pct:.1f}%)

PROCESS STEPS:
{steps_text}

{analysis_section}
Provide your improvement suggestions now.
"""


def generate_vsm_suggestions(value_stream) -> str:
    """Generate improvement suggestions for a VSM based on its step data.

    Returns plain text suggestions. Raises RuntimeError if AI is not configured.
    """
    steps = value_stream.steps.select_related("category").all()

    if not steps:
        raise ValueError("Este VSM no tiene pasos definidos.")

    # Build step descriptions
    step_lines = []
    for s in steps:
        cat_name = s.category.name if s.category else "Sin categoría"
        line = (
            f"  {s.order}. {s.name} [{cat_name}] — "
            f"Trabajo: {s.work_time}h, Espera: {s.wait_time}h, "
            f"Loop: {s.loop_factor*100:.0f}% (+{s.loop_work_extra}h/loop), "
            f"Personas: {s.num_people}, Flujo: {s.flow_type}, "
            f"Fila: {s.row}"
        )
        if s.description:
            line += f"\n     Descripción: {s.description}"
        step_lines.append(line)

    # Compute totals
    lead_time = sum(s.total_time for s in steps)
    total_work = sum(s.work_time for s in steps)
    total_loop = sum(s.loop_time for s in steps)
    total_wait = sum(s.wait_time for s in steps)

    analysis_section = ""
    if value_stream.ai_analysis:
        analysis_section = (
            f"ANÁLISIS PREVIO DE LA IA:\n{value_stream.ai_analysis}\n"
        )

    user_msg = SUGGESTIONS_USER_PROMPT.format(
        project_name=value_stream.project.name if value_stream.project else "Sin proyecto",
        vsm_name=value_stream.name,
        vsm_description=value_stream.description or "(sin descripción)",
        lead_time=lead_time,
        total_work=total_work,
        work_pct=(total_work / lead_time * 100) if lead_time else 0,
        total_loop=total_loop,
        loop_pct=(total_loop / lead_time * 100) if lead_time else 0,
        total_wait=total_wait,
        wait_pct=(total_wait / lead_time * 100) if lead_time else 0,
        steps_text="\n".join(step_lines),
        analysis_section=analysis_section,
    )

    client, model = _get_openai_client()
    config = _get_ai_config()

    logger.info(
        "Calling LLM for VSM suggestions (vsm=%s, model=%s, steps=%d)",
        value_stream.slug, model, len(steps),
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SUGGESTIONS_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=config.temperature if config else 0.3,
        max_tokens=config.max_tokens if config else 4000,
    )

    result = completion.choices[0].message.content.strip()
    logger.info("LLM suggestions received (%d chars)", len(result))
    return result
