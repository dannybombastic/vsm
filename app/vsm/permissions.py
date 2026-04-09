from .models import Project, ProjectMembership


def get_user_projects(user):
    """Return queryset of projects the user has access to.
    Superusers see all projects.
    """
    if user.is_superuser:
        return Project.objects.all()
    return Project.objects.filter(memberships__user=user)


def get_user_role(user, project):
    """Return the user's role string for a project, or None.
    Superusers get 'admin'.
    """
    if user.is_superuser:
        return "admin"
    try:
        m = ProjectMembership.objects.get(user=user, project=project)
        return m.role
    except ProjectMembership.DoesNotExist:
        return None


def user_can_view(user, project):
    """User has any role on the project (viewer+)."""
    return get_user_role(user, project) is not None


def user_can_edit(user, project):
    """User can fill/edit/delete questionnaires (editor+)."""
    return get_user_role(user, project) in ("editor", "project_manager", "admin")


def user_can_manage(user, project):
    """User can generate VSMs, manage project resources (project_manager+)."""
    return get_user_role(user, project) in ("project_manager", "admin")
