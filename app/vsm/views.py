import json
import logging
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from .models import Category, FormResponse, Question, ValueStream, ProcessStep, Project, Diagram
from .forms import DynamicQuestionnaireForm
from .permissions import get_user_projects, get_user_role, user_can_view, user_can_edit, user_can_manage
from .services.ai_generator import ai_is_configured

logger = logging.getLogger(__name__)


@login_required
def index(request):
    """Landing page: app usage flow diagram + navigation links."""
    return render(request, "vsm/index.html")


@login_required
def questionnaire(request, slug, project_slug=None):
    """Display / process a dynamic questionnaire for a category, optionally within a project."""
    category = get_object_or_404(Category, slug=slug)
    project = get_object_or_404(Project, slug=project_slug) if project_slug else None

    # Permission check: project-scoped questionnaires require editor+ role
    if project and not user_can_edit(request.user, project):
        raise PermissionDenied
    sections = category.sections.prefetch_related("questions").all()

    if request.method == "POST":
        form = DynamicQuestionnaireForm(request.POST, category=category)
        if form.is_valid():
            data = {}
            for key, value in form.cleaned_data.items():
                if key in ("respondent_name", "respondent_role"):
                    continue
                data[key] = value
            FormResponse.objects.create(
                category=category,
                project=project,
                respondent_name=form.cleaned_data["respondent_name"],
                respondent_role=form.cleaned_data["respondent_role"],
                data=data,
            )
            if project:
                return redirect("vsm:project_thank_you", project_slug=project.slug, slug=slug)
            return redirect("vsm:thank_you", slug=slug)
    else:
        form = DynamicQuestionnaireForm(category=category)

    # Build section metadata for template rendering
    section_info = []
    for sec in sections:
        questions = []
        for q in sec.questions.all():
            questions.append({
                "key": q.key,
                "label": q.label,
                "type": q.question_type,
                "options": q.options,
                "field": form[q.key],
            })
        section_info.append({
            "code": sec.code,
            "title": sec.title,
            "questions": questions,
        })

    return render(request, "vsm/form.html", {
        "category": category,
        "project": project,
        "form": form,
        "sections": section_info,
    })


@login_required
def thank_you(request, slug, project_slug=None):
    category = get_object_or_404(Category, slug=slug)
    project = get_object_or_404(Project, slug=project_slug) if project_slug else None
    return render(request, "vsm/thank_you.html", {"category": category, "project": project})


@login_required
def api_responses(request, slug):
    """JSON API: return response summary for a category."""
    category = get_object_or_404(Category, slug=slug)
    # Filter to user's projects only
    user_projects = get_user_projects(request.user)
    responses = category.responses.filter(project__in=user_projects).values(
        "respondent_name", "respondent_role", "submitted_at"
    )
    return JsonResponse({"category": category.name, "responses": list(responses)})


@login_required
def vsm_map(request, slug):
    """Render the full Value Stream Map visualization."""
    vs = get_object_or_404(ValueStream, slug=slug)

    # Permission check: user must have access to the project
    if vs.project and not user_can_view(request.user, vs.project):
        raise PermissionDenied

    steps = vs.steps.select_related("category").all()

    # Separate by row
    rows = defaultdict(list)
    for step in steps:
        rows[step.row].append(step)

    # Build category summary table
    cat_summary = defaultdict(lambda: {
        "work_time": 0, "loop_time": 0, "wait_time": 0, "total": 0,
        "color": "#999", "name": "Sin categoría",
    })
    for step in steps:
        key = step.category.slug if step.category else "_none"
        cat_summary[key]["name"] = step.category.name if step.category else "Sin categoría"
        cat_summary[key]["color"] = step.category.color if step.category else "#999"
        cat_summary[key]["work_time"] += step.work_time
        cat_summary[key]["loop_time"] += step.loop_time
        cat_summary[key]["wait_time"] += step.wait_time
        cat_summary[key]["total"] += step.total_time

    # Grand totals
    lead_time = sum(s.total_time for s in steps)
    total_work = sum(s.work_time for s in steps)
    total_loop = sum(s.loop_time for s in steps)
    total_wait = sum(s.wait_time for s in steps)

    # Percentages
    for data in cat_summary.values():
        data["work_pct"] = (data["work_time"] / lead_time * 100) if lead_time else 0
        data["loop_pct"] = (data["loop_time"] / lead_time * 100) if lead_time else 0
        data["wait_pct"] = (data["wait_time"] / lead_time * 100) if lead_time else 0
        data["total_pct"] = (data["total"] / lead_time * 100) if lead_time else 0

    # Sort summaries by category order
    cat_order = {c.slug: c.order for c in Category.objects.all()}
    sorted_summary = sorted(
        cat_summary.items(),
        key=lambda x: cat_order.get(x[0], 99),
    )

    # Prepare step data for template with computed fields
    step_rows = {}
    for row_num, row_steps in sorted(rows.items()):
        step_rows[row_num] = [{
            "name": s.name,
            "category_name": s.category.name if s.category else "",
            "color": s.category.color if s.category else "#999",
            "work_time": s.work_time,
            "wait_time": s.wait_time,
            "loop_factor": s.loop_factor,
            "loop_time": s.loop_time,
            "effective_work": s.effective_work_time,
            "total_time": s.total_time,
            "num_people": s.num_people,
            "flow_type": s.flow_type,
            "description": s.description,
        } for s in row_steps]

    return render(request, "vsm/vsm_map.html", {
        "vs": vs,
        "step_rows": dict(step_rows),
        "summary": sorted_summary,
        "lead_time": lead_time,
        "total_work": total_work,
        "total_loop": total_loop,
        "total_wait": total_wait,
        "work_pct": (total_work / lead_time * 100) if lead_time else 0,
        "loop_pct": (total_loop / lead_time * 100) if lead_time else 0,
        "wait_pct": (total_wait / lead_time * 100) if lead_time else 0,
        "can_manage": user_can_manage(request.user, vs.project) if vs.project else request.user.is_superuser,
        "ai_configured": ai_is_configured(),
    })


@login_required
@require_POST
def vsm_suggestions(request, slug):
    """Generate AI improvement suggestions for a VSM and save them."""
    from .services.ai_generator import generate_vsm_suggestions

    vs = get_object_or_404(ValueStream, slug=slug)

    if vs.project and not user_can_manage(request.user, vs.project):
        raise PermissionDenied
    elif not vs.project and not request.user.is_superuser:
        raise PermissionDenied

    try:
        suggestions = generate_vsm_suggestions(vs)
        vs.ai_suggestions = suggestions
        vs.save(update_fields=["ai_suggestions"])
    except Exception as exc:
        logger.exception("Error generating suggestions for VSM %s", vs.slug)
        # Redirect back; user will see no suggestions appeared

    return redirect("vsm:vsm_map", slug=vs.slug)


@login_required
def vsm_map_list(request):
    """List all available value streams (filtered by user projects)."""
    user_projects = get_user_projects(request.user)
    streams = ValueStream.objects.filter(project__in=user_projects).select_related("project")
    return render(request, "vsm/vsm_map_list.html", {"streams": streams})


# ── Project views ────────────────────────────────────────────────


@login_required
def project_list(request):
    """List projects the user has access to."""
    user_projects = get_user_projects(request.user)
    projects = user_projects.prefetch_related("value_streams", "responses")
    project_data = []
    for p in projects:
        project_data.append({
            "name": p.name,
            "slug": p.slug,
            "color": p.color,
            "description": p.description,
            "vsm_count": p.value_streams.count(),
            "response_count": p.responses.count(),
        })
    return render(request, "vsm/project_list.html", {"projects": project_data})


@login_required
def project_detail(request, slug):
    """Show a project's dashboard: VSM maps + questionnaire responses."""
    project = get_object_or_404(Project, slug=slug)

    # Permission check
    if not user_can_view(request.user, project):
        raise PermissionDenied

    user_role = get_user_role(request.user, project)
    value_streams = project.value_streams.all()
    diagrams = project.diagrams.all()
    default_diagram = project.diagrams.filter(is_default=True).first() or diagrams.first()
    categories = Category.objects.prefetch_related("responses").all()

    cat_data = []
    for cat in categories:
        resp_count = cat.responses.filter(project=project).count()
        cat_data.append({
            "name": cat.name,
            "slug": cat.slug,
            "color": cat.color,
            "response_count": resp_count,
        })

    return render(request, "vsm/project_detail.html", {
        "project": project,
        "value_streams": value_streams,
        "diagrams": diagrams,
        "diagram": default_diagram,
        "categories": cat_data,
        "user_role": user_role,
        "can_edit": user_can_edit(request.user, project),
        "can_manage": user_can_manage(request.user, project),
    })


# ── Diagram views ───────────────────────────────────────────────


@login_required
def diagram_view(request, slug):
    """Full-page interactive Mermaid diagram viewer with zoom/pan."""
    diagram = get_object_or_404(Diagram, slug=slug)

    # Permission check
    if diagram.project and not user_can_view(request.user, diagram.project):
        raise PermissionDenied

    # Sibling diagrams for navigation (same project)
    siblings = Diagram.objects.filter(project=diagram.project).exclude(pk=diagram.pk)
    return render(request, "vsm/diagram_view.html", {
        "diagram": diagram,
        "siblings": siblings,
    })


# ── AI VSM Generation views ─────────────────────────────────────


@login_required
def generate_vsm_view(request, slug):
    """AI-powered VSM generation page: preview responses, generate, preview result."""
    from .services.ai_generator import ai_is_configured

    project = get_object_or_404(Project, slug=slug)

    # Permission check: project_manager+ required
    if not user_can_manage(request.user, project):
        raise PermissionDenied

    categories = Category.objects.all()
    ai_configured = ai_is_configured()

    # Response summary per category
    response_summary = []
    total_responses = 0
    for cat in categories:
        count = FormResponse.objects.filter(project=project, category=cat).count()
        response_summary.append({"name": cat.name, "slug": cat.slug, "color": cat.color, "count": count})
        total_responses += count

    context = {
        "project": project,
        "response_summary": response_summary,
        "total_responses": total_responses,
        "ai_configured": ai_configured,
        "generated": None,
        "error": None,
    }

    if request.method == "POST" and "generate" in request.POST:
        if not ai_configured:
            context["error"] = (
                "La IA no está configurada. Ve a Admin → AI Configuration "
                "para introducir tu API key y endpoint."
            )
        elif total_responses == 0:
            context["error"] = (
                "No hay respuestas de cuestionarios para este proyecto. "
                "Los equipos deben rellenar los cuestionarios primero."
            )
        else:
            try:
                from .services.ai_generator import generate_vsm
                result = generate_vsm(project)
                context["generated"] = result
                context["generated_json"] = json.dumps(result, ensure_ascii=False)
            except Exception as exc:
                logger.exception("Error generating VSM for project %s", project.slug)
                context["error"] = f"Error al generar el VSM: {exc}"

    return render(request, "vsm/generate_vsm.html", context)


@login_required
@require_POST
def save_generated_vsm(request, slug):
    """Save an AI-generated VSM to the database."""
    project = get_object_or_404(Project, slug=slug)

    # Permission check: project_manager+ required
    if not user_can_manage(request.user, project):
        raise PermissionDenied

    raw_json = request.POST.get("vsm_json", "")
    if not raw_json:
        return redirect("vsm:generate_vsm", slug=project.slug)

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return redirect("vsm:generate_vsm", slug=project.slug)

    # Ensure unique slug
    base_slug = slugify(data.get("name", f"{project.name}-ai-vsm"))
    final_slug = base_slug
    counter = 1
    while ValueStream.objects.filter(slug=final_slug).exists():
        final_slug = f"{base_slug}-{counter}"
        counter += 1

    vs = ValueStream.objects.create(
        name=data.get("name", f"{project.name} – AI Generated VSM"),
        slug=final_slug,
        project=project,
        description=data.get("description", ""),
        generation_method="ai",
        ai_analysis=data.get("analysis", ""),
    )

    # Link source responses
    response_ids = data.get("response_ids", [])
    if response_ids:
        vs.source_responses.set(
            FormResponse.objects.filter(pk__in=response_ids, project=project)
        )

    # Create process steps
    cat_map = {c.slug: c for c in Category.objects.all()}
    for step_data in data.get("steps", []):
        ProcessStep.objects.create(
            value_stream=vs,
            name=step_data.get("name", "Unnamed Step"),
            category=cat_map.get(step_data.get("category_slug")),
            order=step_data.get("order", 0),
            row=step_data.get("row", 0),
            work_time=float(step_data.get("work_time", 0)),
            wait_time=float(step_data.get("wait_time", 0)),
            loop_factor=float(step_data.get("loop_factor", 0)),
            loop_work_extra=float(step_data.get("loop_work_extra", 0)),
            num_people=int(step_data.get("num_people", 1)),
            flow_type=step_data.get("flow_type", "push"),
            description=step_data.get("description", ""),
        )

    return redirect("vsm:vsm_map", slug=vs.slug)


# ── Response management views ────────────────────────────────────


@login_required
def response_list(request, project_slug, slug):
    """List all responses for a project + category, with edit/delete links."""
    project = get_object_or_404(Project, slug=project_slug)

    if not user_can_view(request.user, project):
        raise PermissionDenied

    category = get_object_or_404(Category, slug=slug)
    responses = FormResponse.objects.filter(project=project, category=category)
    return render(request, "vsm/response_list.html", {
        "project": project,
        "category": category,
        "responses": responses,
        "can_edit": user_can_edit(request.user, project),
    })


@login_required
def response_edit(request, project_slug, pk):
    """Edit an existing questionnaire response, pre-populating the form."""
    project = get_object_or_404(Project, slug=project_slug)

    if not user_can_edit(request.user, project):
        raise PermissionDenied

    response_obj = get_object_or_404(FormResponse, pk=pk, project=project)
    category = response_obj.category
    sections = category.sections.prefetch_related("questions").all()

    if request.method == "POST":
        form = DynamicQuestionnaireForm(request.POST, category=category)
        if form.is_valid():
            data = {}
            for key, value in form.cleaned_data.items():
                if key in ("respondent_name", "respondent_role"):
                    continue
                data[key] = value
            response_obj.respondent_name = form.cleaned_data["respondent_name"]
            response_obj.respondent_role = form.cleaned_data["respondent_role"]
            response_obj.data = data
            response_obj.save()
            return redirect(
                "vsm:response_list",
                project_slug=project.slug,
                slug=category.slug,
            )
    else:
        # Build initial data from saved response
        initial = {
            "respondent_name": response_obj.respondent_name,
            "respondent_role": response_obj.respondent_role,
        }
        for key, value in response_obj.data.items():
            # Table fields are stored as list of dicts; convert to JSON string
            # so the hidden input has a value that JS can parse.
            if isinstance(value, list):
                initial[key] = json.dumps(value, ensure_ascii=False)
            else:
                initial[key] = value
        form = DynamicQuestionnaireForm(initial=initial, category=category)

    # Build section metadata (same pattern as questionnaire view)
    section_info = []
    for sec in sections:
        questions = []
        for q in sec.questions.all():
            questions.append({
                "key": q.key,
                "label": q.label,
                "type": q.question_type,
                "options": q.options,
                "field": form[q.key],
            })
        section_info.append({
            "code": sec.code,
            "title": sec.title,
            "questions": questions,
        })

    return render(request, "vsm/form.html", {
        "category": category,
        "project": project,
        "form": form,
        "sections": section_info,
        "editing": True,
        "response_pk": response_obj.pk,
    })


@login_required
@require_POST
def response_delete(request, project_slug, pk):
    """Delete a questionnaire response (POST only)."""
    project = get_object_or_404(Project, slug=project_slug)

    if not user_can_edit(request.user, project):
        raise PermissionDenied

    response_obj = get_object_or_404(FormResponse, pk=pk, project=project)
    category_slug = response_obj.category.slug
    response_obj.delete()
    return redirect(
        "vsm:response_list",
        project_slug=project.slug,
        slug=category_slug,
    )
