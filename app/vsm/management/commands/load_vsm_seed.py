"""
Management command to seed a Value Stream Map with ATHINA development cycle data.
Creates a complete value stream with process steps, timing metrics, and loop factors.

Usage:
    python manage.py load_vsm_seed
"""

from django.core.management.base import BaseCommand
from vsm.models import Category, ValueStream, ProcessStep, Project


# Step definitions: (name, category_slug, row, work_time, wait_time, loop_factor, loop_work_extra, num_people, flow_type)
ATHINA_STEPS = [
    # ── Row 0: Main development flow ──
    ("Recepción y triaje del requisito", "management", 0, 2.0, 8.0, 0, 0, 1, "push"),
    ("Análisis y estimación", "agile-scrum", 0, 8.0, 16.0, 0.3, 4.0, 2, "push"),
    ("Diseño funcional y técnico", "agile-scrum", 0, 16.0, 24.0, 0.2, 6.0, 2, "push"),
    ("Planificación Sprint", "agile-scrum", 0, 4.0, 8.0, 0, 0, 3, "push"),
    ("Desarrollo Backend", "developers", 0, 40.0, 8.0, 0.3, 12.0, 3, "push"),
    ("Desarrollo Frontend", "developers", 0, 32.0, 4.0, 0.25, 8.0, 2, "push"),
    ("Code Review", "developers", 0, 4.0, 16.0, 0.8, 3.0, 2, "push"),
    ("Unit Tests & SonarQube", "qa-testing", 0, 2.0, 4.0, 0.1, 2.0, 1, "push"),
    # ── Row 1: QA & Deployment flow ──
    ("Pruebas funcionales QA", "qa-testing", 1, 24.0, 16.0, 0.3, 8.0, 2, "push"),
    ("Pruebas de regresión", "qa-testing", 1, 16.0, 8.0, 0.15, 4.0, 2, "push"),
    ("Docker Build & Qualys Scan", "devops-platform", 1, 1.0, 4.0, 0.05, 1.0, 1, "push"),
    ("Deploy a DEV/TEST", "devops-platform", 1, 0.5, 2.0, 0.1, 0.5, 1, "push"),
    ("Pruebas UAT", "qa-testing", 1, 16.0, 24.0, 0.2, 6.0, 3, "push"),
    ("Deploy a UAT/PRD", "devops-platform", 1, 1.0, 8.0, 0.05, 0.5, 1, "push"),
    ("Validación post-deploy", "devops-platform", 1, 2.0, 4.0, 0.1, 1.0, 1, "push"),
    ("Reporting y cierre", "management", 1, 4.0, 16.0, 0, 0, 1, "push"),
]


class Command(BaseCommand):
    help = "Seed the ATHINA development cycle Value Stream Map with realistic timing data."

    def handle(self, *args, **options):
        # Create or retrieve the default ATHINA project
        project, _ = Project.objects.update_or_create(
            slug="athina",
            defaults={
                "name": "ATHINA",
                "description": "Proyecto principal ATHINA LOT1 – plataforma de gestión para HADEA.",
                "color": "#dc2626",
            },
        )

        vs, created = ValueStream.objects.update_or_create(
            slug="athina-dev-cycle",
            defaults={
                "name": "ATHINA – Ciclo de Desarrollo",
                "project": project,
                "description": (
                    "Mapa de flujo de valor del ciclo completo de desarrollo de ATHINA: "
                    "desde la recepción de requisitos hasta el despliegue en producción. "
                    "Incluye métricas de tiempos de proceso, espera y bucles de retrabajo."
                ),
            },
        )

        if not created:
            vs.steps.all().delete()
            self.stdout.write(self.style.WARNING("ValueStream existente actualizado; pasos regenerados."))

        # Pre-fetch categories
        cat_map = {}
        for cat in Category.objects.all():
            cat_map[cat.slug] = cat

        steps_created = 0
        for i, (name, cat_slug, row, wt, wait, lf, lwe, ppl, ft) in enumerate(ATHINA_STEPS, start=1):
            cat = cat_map.get(cat_slug)
            if not cat:
                self.stdout.write(self.style.WARNING(f"Categoría '{cat_slug}' no encontrada; paso '{name}' sin categoría."))

            ProcessStep.objects.create(
                value_stream=vs,
                name=name,
                category=cat,
                order=i,
                row=row,
                work_time=wt,
                wait_time=wait,
                loop_factor=lf,
                loop_work_extra=lwe,
                num_people=ppl,
                flow_type=ft,
            )
            steps_created += 1

        lead = vs.lead_time
        self.stdout.write(self.style.SUCCESS(
            f"✅ ValueStream '{vs.name}' creado con {steps_created} pasos. Lead Time: {lead:.1f}h"
        ))
