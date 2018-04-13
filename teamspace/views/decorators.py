"""
View Decorators

For more information on decorators, see
https://docs.djangoproject.com/en/1.10/topics/http/decorators/

For more information on controllers (views), see
https://docs.djangoproject.com/en/1.10/#the-view-layer

For the full list of requests and their responses, see
https://docs.djangoproject.com/en/1.10/ref/request-response/
"""
from django.http import Http404
from django.shortcuts import redirect
from teamspace.models import Organization
from teamspace.models import OrganizationMembership
from teamspace.models import Team
from teamspace.models import TeamMembership


def require_authenticated(closure):
    """
    Requires that the user is logged in.

    :param closure:
    :return: check
    """
    def check(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('frontend:home')
        else:
            return closure(request, *args, **kwargs)
    return check


def require_unauthenticated(closure):
    """
    Requires that the user is not logged in.

    :param closure:
    :return: check
    """
    def check(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('dashboard:home')
        else:
            return closure(request, *args, **kwargs)
    return check


def require_org_member(closure):
    """
    Requires that the user is a member of the organization.

    :param closure:
    :return:
    """
    def check(request, id, *args, **kwargs):
        try:
            OrganizationMembership.objects.get(user_id=request.user.id, organization_id=id)
        except OrganizationMembership.DoesNotExist:
            raise Http404()
        return closure(request, id, *args, **kwargs)
    return check


def require_org_owner(closure):
    """
    Requires that the user is the owner of the organization.

    :param closure:
    :return:
    """
    def check(request, id, *args, **kwargs):
        try:
            organization = Organization.objects.get(pk=id)
            if organization.owner_id != request.user.id:
                raise Http404()
        except Organization.DoesNotExist:
            raise Http404()
        return closure(request, id, *args, **kwargs)
    return check


def require_team_member(closure):
    """
    Requires that the user is a member of the team.

    :param closure:
    :return:
    """
    def check(request, id, *args, **kwargs):
        try:
            TeamMembership.objects.get(user_id=request.user.id, team_id=id)
        except TeamMembership.DoesNotExist:
            raise Http404()
        return closure(request, id, *args, **kwargs)
    return check


def require_team_owner(closure):
    """
    Requires that the user is the owner of the team.

    :param closure:
    :return:
    """
    def check(request, id, *args, **kwargs):
        try:
            team = Team.objects.get(pk=id)
            if team.owner_id != request.user.id:
                raise Http404()
        except Team.DoesNotExist:
            raise Http404()
        return closure(request, id, *args, **kwargs)
    return check
