"""
Management command to generate realistic test data for the VSM app.
Creates: a second project, additional ValueStream, and sample questionnaire responses.

Usage:
    python manage.py load_test_data
"""

import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from vsm.models import Category, Question, FormResponse, Project, ValueStream, ProcessStep


# ── Fake respondents ────────────────────────────────────────────

RESPONDENTS = [
    ("Carlos García", "Senior Backend Developer"),
    ("María López", "Frontend Lead"),
    ("Juan Martínez", "QA Engineer"),
    ("Ana Rodríguez", "UX Designer"),
    ("Pedro Sánchez", "Data Analyst"),
    ("Laura Fernández", "Scrum Master"),
    ("Miguel Torres", "Project Manager"),
    ("Elena Ruiz", "DevOps Engineer"),
    ("Pablo Díaz", "Tech Lead"),
    ("Sofía Moreno", "Security Analyst"),
    ("Diego Herrera", "Full Stack Developer"),
    ("Isabel Navarro", "QA Lead"),
    ("Andrés Molina", "Data Engineer"),
    ("Carmen Ortiz", "Product Owner"),
    ("Raúl Jiménez", "Site Reliability Engineer"),
]

# ── Text-answer pools by question type patterns ─────────────────

TEAM_NAMES = [
    "Backend Core Team", "Frontend Squad", "QA Automation Team",
    "UX Research Team", "Data Platform Team", "Agile Office",
    "Platform Engineering", "Security & Compliance",
]

SHORT_ANSWERS = {
    "team": ["Backend Core", "Frontend Squad", "QA Automation", "Data Platform", "Platform Eng"],
    "client": ["Product Owner", "End users (HADEA)", "Dev team", "QA team", "Stakeholders"],
    "supplier": ["Jira stories", "Figma designs", "API specs from architects", "Data from Synapse"],
    "tool": ["IntelliJ IDEA", "VS Code", "Azure DevOps", "SonarQube", "Postman", "Selenium", "JMeter"],
    "duration": ["2-3 hours", "1 day", "2-4 days", "1 sprint (2 weeks)", "30 minutes", "4 hours"],
    "frequency": ["Every sprint", "Daily", "Weekly", "On demand", "Per release", "Bi-weekly"],
    "percentage": ["85%", "90%", "75%", "95%", "70%", "80%", "60%"],
}

LONG_ANSWERS = [
    "El proceso comienza con la recepción del requisito desde el Product Owner a través de Jira. "
    "Se realiza un análisis técnico inicial, se estima en planning poker y se asigna al sprint.",
    "Utilizamos un flujo GitFlow con ramas feature, develop y main. Cada PR requiere al menos "
    "2 aprobaciones y pasa por SonarQube antes del merge.",
    "Las pruebas se ejecutan automáticamente en el pipeline CI/CD. Incluyen unit tests, "
    "integration tests y smoke tests. Los resultados se reportan en Azure DevOps.",
    "El despliegue sigue una estrategia blue-green con Container Apps. Primero se despliega "
    "en desarrollo, luego test, UAT y finalmente producción con aprobación manual.",
    "Se identifican los principales cuellos de botella en las esperas por revisión de código "
    "y en la aprobación de PRs que suelen tardar 1-2 días.",
    "El equipo realiza retrospectivas cada sprint donde se identifican mejoras. "
    "Se utiliza un board de Kaizen para seguimiento de acciones de mejora.",
    "La comunicación entre equipos se realiza a través de Teams y reuniones diarias de 15 min. "
    "Los bloqueos se escalan inmediatamente al Scrum Master.",
    "La documentación técnica se mantiene en Confluence y se actualiza con cada release. "
    "Los ADRs se registran para decisiones arquitectónicas importantes.",
    "El monitoreo se realiza con Azure Application Insights y Grafana. Se tienen alertas "
    "configuradas para errores 5xx, latencia alta y uso de recursos.",
    "La gestión de secretos se hace con Azure Key Vault y Managed Identities. "
    "No se almacenan credenciales en código ni en variables de entorno directamente.",
]

CHECKLIST_OPTIONS_POOL = {
    "dev_c4": ["Git/GitHub", "CI/CD Pipeline", "SonarQube", "Docker", "Kubernetes"],
    "dev_d2": ["Automated tests", "Manual testing", "Code review", "Static analysis"],
    "qa_c4": ["Selenium", "JUnit", "Postman", "JMeter", "Azure DevOps Test Plans"],
    "qa_d2": ["Shift-left testing", "BDD/TDD", "Exploratory testing", "Performance testing"],
    "devops_c4": ["Terraform", "Docker", "Kubernetes/AKS", "Azure CLI", "Helm", "ArgoCD"],
}

# ── Second project + VSM ─────────────────────────────────────────

SECOND_PROJECT = {
    "name": "ATHINA LOT2",
    "slug": "athina-lot2",
    "description": "Módulo de Analytics y Reporting avanzado para HADEA – LOT2.",
    "color": "#0891b2",
}

LOT2_STEPS = [
    ("Requisitos BI", "management", 0, 4.0, 12.0, 0.15, 2.0, 1, "push"),
    ("Diseño de data model", "data-analytics", 0, 12.0, 8.0, 0.2, 4.0, 2, "push"),
    ("ETL Development", "data-analytics", 0, 24.0, 16.0, 0.3, 8.0, 2, "push"),
    ("Dashboard Development", "developers", 0, 20.0, 8.0, 0.25, 6.0, 2, "push"),
    ("QA de datos", "qa-testing", 0, 8.0, 12.0, 0.2, 3.0, 1, "push"),
    ("Deploy Synapse", "devops-platform", 0, 2.0, 4.0, 0.1, 1.0, 1, "push"),
    ("Validación usuario", "management", 0, 4.0, 24.0, 0.3, 2.0, 2, "push"),
]


def _generate_answer(question):
    """Generate a plausible answer based on question type and key."""
    if question.question_type == "text":
        key_lower = question.key.lower()
        if "name" in key_lower or "team" in key_lower:
            return random.choice(SHORT_ANSWERS["team"])
        if "client" in key_lower or "consumer" in key_lower:
            return random.choice(SHORT_ANSWERS["client"])
        if "supplier" in key_lower or "feed" in key_lower:
            return random.choice(SHORT_ANSWERS["supplier"])
        if "duration" in key_lower or "time" in key_lower:
            return random.choice(SHORT_ANSWERS["duration"])
        if "frequency" in key_lower or "often" in key_lower:
            return random.choice(SHORT_ANSWERS["frequency"])
        return random.choice(SHORT_ANSWERS["tool"])

    elif question.question_type == "textarea":
        return random.choice(LONG_ANSWERS)

    elif question.question_type == "checklist":
        pool = CHECKLIST_OPTIONS_POOL.get(question.key)
        if pool:
            return random.sample(pool, k=min(random.randint(2, 4), len(pool)))
        if question.options:
            opts = question.options if isinstance(question.options, list) else []
            if opts:
                return random.sample(opts, k=min(random.randint(1, 3), len(opts)))
        return ["Option A", "Option B"]

    elif question.question_type == "table":
        cols = (question.options or {}).get("columns", ["Col1", "Col2"])
        rows_data = []
        for i in range(random.randint(2, 4)):
            row = {}
            for col in cols:
                col_lower = col.lower()
                if "step" in col_lower or "who" in col_lower:
                    row[col] = f"Paso {i+1}" if "step" in col_lower else random.choice(["Dev", "QA", "PO", "DevOps"])
                elif "duration" in col_lower or "time" in col_lower or "wait" in col_lower:
                    row[col] = random.choice(SHORT_ANSWERS["duration"])
                elif "%" in col_lower or "accurate" in col_lower:
                    row[col] = random.choice(SHORT_ANSWERS["percentage"])
                else:
                    row[col] = f"Valor {i+1}"
            rows_data.append(row)
        return rows_data

    return "N/A"


class Command(BaseCommand):
    help = "Generate realistic test data: responses, a second project, and an additional VSM."

    def handle(self, *args, **options):
        random.seed(42)  # Reproducible

        # ── 1. Second project + VSM ──────────────────────────────
        project2, _ = Project.objects.update_or_create(
            slug=SECOND_PROJECT["slug"],
            defaults={
                "name": SECOND_PROJECT["name"],
                "description": SECOND_PROJECT["description"],
                "color": SECOND_PROJECT["color"],
            },
        )
        self.stdout.write(f"  Project: {project2.name}")

        vs2, created = ValueStream.objects.update_or_create(
            slug="athina-lot2-analytics",
            defaults={
                "name": "ATHINA LOT2 – Analytics & Reporting",
                "project": project2,
                "description": "Flujo de desarrollo de dashboards y ETL para el módulo de analytics.",
            },
        )
        if not created:
            vs2.steps.all().delete()

        cat_map = {c.slug: c for c in Category.objects.all()}
        for i, (name, cat_slug, row, wt, wait, lf, lwe, ppl, ft) in enumerate(LOT2_STEPS, 1):
            ProcessStep.objects.create(
                value_stream=vs2, name=name, category=cat_map.get(cat_slug),
                order=i, row=row, work_time=wt, wait_time=wait,
                loop_factor=lf, loop_work_extra=lwe, num_people=ppl, flow_type=ft,
            )
        self.stdout.write(f"  VSM: {vs2.name} ({vs2.steps.count()} pasos, Lead: {vs2.lead_time:.1f}h)")

        # ── 2. Generate questionnaire responses ──────────────────
        athina_project = Project.objects.filter(slug="athina").first()
        projects = [athina_project, project2]

        categories = list(Category.objects.prefetch_related("sections__questions").all())
        responses_created = 0

        for cat in categories:
            questions = list(
                Question.objects.filter(section__category=cat)
                .select_related("section")
                .order_by("section__order", "order")
            )

            # 2-4 responses per category per project
            for project in projects:
                if not project:
                    continue
                num_responses = random.randint(2, 4)
                respondents = random.sample(RESPONDENTS, k=num_responses)

                for name, role in respondents:
                    data = {}
                    for q in questions:
                        data[q.key] = _generate_answer(q)

                    FormResponse.objects.create(
                        category=cat,
                        project=project,
                        respondent_name=name,
                        respondent_role=role,
                        data=data,
                    )
                    responses_created += 1

            # Also 1 response without project (global)
            gname, grole = random.choice(RESPONDENTS)
            gdata = {q.key: _generate_answer(q) for q in questions}
            FormResponse.objects.create(
                category=cat, project=None,
                respondent_name=gname, respondent_role=grole, data=gdata,
            )
            responses_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Test data loaded: {responses_created} responses across "
            f"{len(categories)} categories and {len([p for p in projects if p])+1} contexts (2 projects + global)"
        ))
