from django.conf import settings
from django.db import models


# ── AI Configuration (singleton) ────────────────────────────────


class AIConfiguration(models.Model):
    """Singleton: AI provider settings for VSM generation – editable from Admin."""

    PROVIDERS = [
        ("openai", "OpenAI"),
        ("azure", "Azure OpenAI"),
    ]

    provider = models.CharField(
        max_length=10, choices=PROVIDERS, default="openai",
        help_text="AI provider to use for VSM generation",
    )
    api_key = models.CharField(
        max_length=256,
        help_text="API key for the selected provider",
    )
    endpoint = models.URLField(
        max_length=300, blank=True, default="",
        help_text="Custom endpoint URL. Leave blank for default OpenAI (https://api.openai.com/v1). "
                  "For Azure, use: https://YOUR-RESOURCE.openai.azure.com/",
    )
    model_name = models.CharField(
        max_length=100, default="gpt-4o",
        help_text="Model / deployment name (e.g. gpt-4o, gpt-4o-mini)",
    )
    api_version = models.CharField(
        max_length=20, blank=True, default="2024-06-01",
        help_text="API version (Azure OpenAI only)",
    )
    temperature = models.FloatField(
        default=0.3,
        help_text="LLM temperature (0.0 = deterministic, 1.0 = creative)",
    )
    max_tokens = models.PositiveIntegerField(
        default=4000,
        help_text="Maximum tokens in LLM response",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to disable AI generation",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AI Configuration"
        verbose_name_plural = "AI Configuration"

    def __str__(self):
        return f"AI Config – {self.get_provider_display()} ({self.model_name})"

    def save(self, *args, **kwargs):
        # Singleton: force pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Return the singleton instance or None."""
        try:
            return cls.objects.get(pk=1)
        except cls.DoesNotExist:
            return None


# ── Questionnaire models ────────────────────────────────────────


class Category(models.Model):
    """A VSM team/role category (e.g. Developers, QA, DevOps)."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    color = models.CharField(max_length=7, default="#6366f1", help_text="Hex color for diagrams")
    order = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Section(models.Model):
    """A section inside a category questionnaire (A-F)."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sections")
    code = models.CharField(max_length=5, help_text="e.g. A, B, C")
    title = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ("category", "code")

    def __str__(self):
        return f"{self.category.slug} / {self.code} – {self.title}"


class Question(models.Model):
    """A single question inside a section."""

    QUESTION_TYPES = [
        ("text", "Text (short)"),
        ("textarea", "Textarea (long)"),
        ("table", "Table (rows × columns)"),
        ("checklist", "Checklist (options)"),
    ]

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="questions")
    key = models.CharField(max_length=60, help_text="Unique key within the category")
    label = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default="text")
    options = models.JSONField(
        blank=True,
        null=True,
        help_text="JSON: columns for table, items for checklist",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"[{self.section.category.slug}] {self.key}"


class Project(models.Model):
    """A project that groups VSM maps and questionnaire responses."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#6366f1", help_text="Hex color badge")
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProjectMembership",
        related_name="projects",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    """Links a user to a project with a specific role."""

    ROLE_CHOICES = [
        ("viewer", "Viewer"),
        ("editor", "Editor"),
        ("project_manager", "Project Manager"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")

    class Meta:
        unique_together = ("project", "user")
        verbose_name = "Project Membership"
        verbose_name_plural = "Project Memberships"

    def __str__(self):
        return f"{self.user.username} → {self.project.name} ({self.get_role_display()})"


class FormResponse(models.Model):
    """Stores one complete questionnaire submission."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="responses")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="responses",
        null=True, blank=True,
    )
    respondent_name = models.CharField(max_length=200)
    respondent_role = models.CharField(max_length=200, blank=True)
    data = models.JSONField(default=dict, help_text="All answers keyed by question key")
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        prefix = f"[{self.project.name}] " if self.project else ""
        return f"{prefix}{self.category.name} – {self.respondent_name} ({self.submitted_at:%Y-%m-%d})"


# ── Mermaid Diagrams ─────────────────────────────────────────────


class Diagram(models.Model):
    """A Mermaid diagram associated with a project, managed from admin."""

    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="diagrams",
        null=True, blank=True, help_text="Leave blank for global diagrams",
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    mermaid_code = models.TextField(help_text="Mermaid diagram code (graph LR, flowchart TD, etc.)")
    is_default = models.BooleanField(
        default=False,
        help_text="If checked, this diagram is shown as the main diagram for the project",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "-updated_at"]

    def __str__(self):
        prefix = f"[{self.project.name}] " if self.project else "[Global] "
        return f"{prefix}{self.name}"


# ── VSM Map models ──────────────────────────────────────────────


class ValueStream(models.Model):
    """A complete value stream map."""

    GENERATION_METHODS = [
        ("manual", "Manual"),
        ("ai", "AI Generated"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="value_streams",
        null=True, blank=True,
    )
    description = models.TextField(blank=True)
    generation_method = models.CharField(
        max_length=10, choices=GENERATION_METHODS, default="manual",
    )
    ai_analysis = models.TextField(
        blank=True, help_text="AI reasoning and analysis summary",
    )
    ai_suggestions = models.TextField(
        blank=True, help_text="AI-generated improvement suggestions based on VSM results",
    )
    source_responses = models.ManyToManyField(
        "FormResponse", blank=True, related_name="derived_value_streams",
        help_text="FormResponses used to generate this VSM",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name

    @property
    def lead_time(self):
        return sum(s.total_time for s in self.steps.all())

    @property
    def total_work_time(self):
        return sum(s.work_time for s in self.steps.all())

    @property
    def total_wait_time(self):
        return sum(s.wait_time for s in self.steps.all())


class ProcessStep(models.Model):
    """A single step in the value stream with timing metrics."""

    PUSH_PULL = [("push", "Push"), ("pull", "Pull")]

    value_stream = models.ForeignKey(ValueStream, on_delete=models.CASCADE, related_name="steps")
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Category/team responsible for this step",
    )
    order = models.PositiveSmallIntegerField(default=0)
    row = models.PositiveSmallIntegerField(
        default=0, help_text="Visual row (0=main flow, 1=secondary flow)"
    )
    work_time = models.FloatField(default=0, help_text="Process/touch time in hours")
    wait_time = models.FloatField(default=0, help_text="Wait/idle time before this step in hours")
    loop_factor = models.FloatField(
        default=0, help_text="Rework loop probability (0-1). E.g. 0.3 = 30% rework"
    )
    loop_work_extra = models.FloatField(
        default=0, help_text="Extra work time per loop iteration in hours"
    )
    num_people = models.PositiveSmallIntegerField(default=1)
    flow_type = models.CharField(max_length=4, choices=PUSH_PULL, default="push")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["row", "order"]

    def __str__(self):
        return f"[{self.value_stream.slug}] {self.order}. {self.name}"

    @property
    def loop_time(self):
        """Extra time added by rework loops."""
        if self.loop_factor > 0:
            return self.loop_work_extra * self.loop_factor
        return 0

    @property
    def effective_work_time(self):
        return self.work_time + self.loop_time

    @property
    def total_time(self):
        return self.effective_work_time + self.wait_time
