from django import forms
from .models import Category, Question


class DynamicQuestionnaireForm(forms.Form):
    """Builds form fields dynamically from the Question model."""

    respondent_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
    )
    respondent_role = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your role"}),
    )

    def __init__(self, *args, category: Category | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if category is None:
            return

        questions = Question.objects.filter(
            section__category=category,
        ).select_related("section").order_by("section__order", "order")

        for q in questions:
            field_name = q.key
            if q.question_type == "text":
                self.fields[field_name] = forms.CharField(
                    label=q.label,
                    required=False,
                    widget=forms.TextInput(attrs={"class": "form-control"}),
                )
            elif q.question_type == "textarea":
                self.fields[field_name] = forms.CharField(
                    label=q.label,
                    required=False,
                    widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
                )
            elif q.question_type == "checklist":
                choices = [(opt, opt) for opt in (q.options or [])]
                self.fields[field_name] = forms.MultipleChoiceField(
                    label=q.label,
                    required=False,
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple(),
                )
            elif q.question_type == "table":
                # Table questions are handled with JS in the template;
                # we store raw JSON from the hidden input.
                self.fields[field_name] = forms.CharField(
                    label=q.label,
                    required=False,
                    widget=forms.HiddenInput(attrs={"class": "table-json-field"}),
                )
