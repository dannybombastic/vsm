"""
Management command to load/sync questions from YAML config into the database.
Idempotent: safe to run multiple times.
"""
from pathlib import Path

import yaml
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from vsm.models import Category, Section, Question


class Command(BaseCommand):
    help = "Load VSM questions from fixtures/questions_config.yaml"

    def handle(self, *args, **options):
        config_path = Path(__file__).resolve().parent.parent.parent / "fixtures" / "questions_config.yaml"

        with open(config_path, "r") as f:
            data = yaml.safe_load(f)

        for cat_data in data["categories"]:
            category, created = Category.objects.update_or_create(
                slug=cat_data["slug"],
                defaults={
                    "name": cat_data["name"],
                    "color": cat_data.get("color", "#6366f1"),
                    "order": cat_data.get("order", 0),
                    "description": cat_data.get("description", ""),
                },
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"  {action} category: {category.name}")

            for sec_data in cat_data.get("sections", []):
                section, _ = Section.objects.update_or_create(
                    category=category,
                    code=sec_data["code"],
                    defaults={
                        "title": sec_data["title"],
                        "order": sec_data.get("order", 0),
                    },
                )

                for q_data in sec_data.get("questions", []):
                    Question.objects.update_or_create(
                        section=section,
                        key=q_data["key"],
                        defaults={
                            "label": q_data["label"],
                            "question_type": q_data.get("type", "text"),
                            "options": q_data.get("options"),
                            "order": q_data.get("order", 0),
                        },
                    )

        total_q = Question.objects.count()
        self.stdout.write(self.style.SUCCESS(f"\n✅ Loaded {total_q} questions across {Category.objects.count()} categories"))
