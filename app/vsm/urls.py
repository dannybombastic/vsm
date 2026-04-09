from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "vsm"

urlpatterns = [
    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="vsm/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("", views.index, name="index"),

    # Projects
    path("projects/", views.project_list, name="project_list"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),

    # Diagrams
    path("diagram/<slug:slug>/", views.diagram_view, name="diagram_view"),

    # AI VSM Generation
    path("projects/<slug:slug>/generate-vsm/", views.generate_vsm_view, name="generate_vsm"),
    path("projects/<slug:slug>/save-generated-vsm/", views.save_generated_vsm, name="save_generated_vsm"),

    # Project-scoped questionnaires
    path("projects/<slug:project_slug>/questionnaire/<slug:slug>/", views.questionnaire, name="project_questionnaire"),
    path("projects/<slug:project_slug>/questionnaire/<slug:slug>/thank-you/", views.thank_you, name="project_thank_you"),

    # Response management (view / edit / delete)
    path("projects/<slug:project_slug>/responses/<slug:slug>/", views.response_list, name="response_list"),
    path("projects/<slug:project_slug>/response/<int:pk>/edit/", views.response_edit, name="response_edit"),
    path("projects/<slug:project_slug>/response/<int:pk>/delete/", views.response_delete, name="response_delete"),

    # VSM maps
    path("vsm-map/", views.vsm_map_list, name="vsm_map_list"),
    path("vsm-map/<slug:slug>/", views.vsm_map, name="vsm_map"),
    path("vsm-map/<slug:slug>/suggestions/", views.vsm_suggestions, name="vsm_suggestions"),

    # Global questionnaires (no project)
    path("questionnaire/<slug:slug>/", views.questionnaire, name="questionnaire"),
    path("questionnaire/<slug:slug>/thank-you/", views.thank_you, name="thank_you"),

    # API
    path("api/responses/<slug:slug>/", views.api_responses, name="api_responses"),
]
