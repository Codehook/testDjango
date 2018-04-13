"""
Organization Controller

For more information on controllers (views), see
https://docs.djangoproject.com/en/1.10/#the-view-layer

For the full list of requests and their responses, see
https://docs.djangoproject.com/en/1.10/ref/request-response/
"""
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from teamspace.utils import get_users
from teamspace.utils import format_errors
from teamspace.utils import format_description
from teamspace.models import Team
from teamspace.models import Organization
from teamspace.models import OrganizationMembership
from teamspace.forms.user import AddMember
from teamspace.forms.team import TeamCreateForm
from teamspace.forms.organization import OrganizationEditForm
from teamspace.views.decorators import require_org_owner
from teamspace.views.decorators import require_org_member
from teamspace.views.decorators import require_authenticated


@require_authenticated
@require_org_member
def leave(request, id):
    """
    Deletes the membership record of the queried organization if the user is a member.

    :param request:
    :param id: Organization ID
    :return: redirect
    """

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.get(pk=id)
    except Organization.DoesNotExist:
        raise Http404()

    # Fetch the corresponding organization membership
    try:
        membership = OrganizationMembership.objects.get(user_id=request.user.id, organization_id=organization.id)
    except OrganizationMembership.DoesNotExist:
        raise Http404()

    # Delete the membership and decrement the member count
    if membership:
        membership.delete()
        organization.members -= 1
        organization.save()
        messages.info(request, 'You have left the organization.')

    # Redirect the user back to the organization view
    return redirect('dashboard:organization:view')


@require_authenticated
@require_org_owner
def delete(request, id):
    """
    Deletes the queried organization if the user is the owner.

    :param request:
    :param id: Organization ID
    :return: redirect
    """

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.get(pk=id)
    except Organization.DoesNotExist:
        raise Http404()

    # Make sure the user is the owner
    if organization.owner_id == request.user.id:
        organization.delete()
        messages.info(request, 'The organization has been deleted.')

    # Redirect the user back to the organization view
    return redirect('dashboard:organization:view')


@require_authenticated
@require_org_member
def home(request, id):
    """
    Returns a view with the queried organization and a parsed markdown description.

    :param request:
    :param id: Organization ID
    :return: render
    """

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.get(pk=id)
    except Organization.DoesNotExist:
        raise Http404()

    # Parse the description
    organization.markdown = format_description(organization.description)

    # Give the template a title
    title = organization.name + ': Home'

    # Render the template with the queried data set
    return render(request, 'backend/organization/home.html', {
        'title': title, 'organization': organization,
    })


@require_authenticated
@require_org_member
def users(request, id):
    """
    Returns a view containing a list of members in the queried organization.

    :param request:
    :param id: Organization ID
    :return: render
    """

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=id)
    except Organization.DoesNotExist:
        raise Http404()

    # Get a list of organization members (as users)
    users = get_users(id, 'organization')

    # Give the template a title
    title = organization.name + ': Users'

    # Render the template with the queried data set
    return render(request, 'backend/organization/users.html', {
        'title': title, 'users': users, 'organization': organization,
    })


@require_authenticated
@require_org_member
def teams_view(request, id):
    """
    Returns a view containing a list of teams in the queried organization.

    :param request:
    :param id: Organization ID
    :return: render
    """

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=id)
    except Organization.DoesNotExist:
        raise Http404()

    # TODO: If the user is the organization owner, show all the teams.
    # TODO: If they are not the owner, then only show teams where they are a member.
    # Fetch the corresponding list of teams
    teams = Team.objects.defer('description').filter(parent_id=id)

    # Flash a message if the list of teams is empty
    if not teams:
        messages.info(request, 'Your organization does not have any teams. Go create one!')

    # Give the template a title
    title = organization.name + ': View Teams'

    # Render the template with the queried data set
    return render(request, 'backend/organization/teams_view.html', {
        'title': title, 'teams': teams, 'organization': organization,
    })


@require_authenticated
@require_org_member
def teams_create(request, id):
    """
    Returns a view where users can create a team within the queried organization.

    :param request:
    :param id: Organization ID
    :return: render, redirect
    """

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=id)
    except Organization.DoesNotExist:
        raise Http404()

    # Give the template a title
    title = organization.name + ': Create Team'

    # Handle a POST method
    if request.method == 'POST':

        # Process the post data in the form
        form = TeamCreateForm(request.POST, parent_id=id, owner_id=request.user.id)

        # Check if the form is valid
        if form.is_valid():

            # Create the team
            team = form.save()

            # Post a success message
            messages.success(request, 'Team successfully created.')

            # Redirect to the newly created team
            return redirect('team:home', team.id)

        else:

            # Post an error message
            messages.error(request, format_errors(form.errors))

            # Return with the errors otherwise
            return render(request, 'backend/organization/teams_create.html', {
                'title': title, 'form': form, 'organization': organization,
            })

    # Render the template with the queried data set
    return render(request, 'backend/organization/teams_create.html', {
        'title': title, 'organization': organization,
    })


@require_authenticated
@require_org_owner
def manage_edit(request, id):
    """
    Returns a view where an owner can edit their organization.

    :param request:
    :param id: Organization ID
    :return: render
    """

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.get(pk=id)
    except Organization.DoesNotExist:
        raise Http404()

    # Give the template a title
    title = organization.name + ': Edit'

    # Handle a POST method
    if request.method == 'POST':

        # Update the form with the post data
        form = OrganizationEditForm(request.POST, instance=organization)

        # Check if the form is valid
        if form.is_valid():

            # Update and save the organization
            form.save()

            # Post a success message
            messages.success(request, 'Settings successfully saved.')

        else:

            # Post an error message
            messages.error(request, format_errors(form.errors))

    else:

        # Give the default form
        form = OrganizationEditForm(instance=organization)

    # Render the template with the queried data set
    return render(request, 'backend/organization/manage_edit.html', {
        'title': title, 'form': form, 'organization': organization,
    })


@require_authenticated
@require_org_owner
def manage_users(request, id):
    """
    Returns a view with a list of users and a form to add users.

    :param request:
    :param id: Organization ID
    :return: render
    """

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=id)
    except Organization.DoesNotExist:
        raise Http404()
    form = None

    # Handle a POST method
    if request.method == 'POST':

        # Handle invitations by creating a membership record
        if 'email' in request.POST:

            # Process the email address
            form = AddMember(request.POST, id=id, organization=True)

            # Check if the form is valid
            if form.is_valid():

                # Create the membership record
                form.add_member()
                organization.members += 1
                organization.save()

                # Post a success message
                messages.success(request, 'User successfully added.')

            else:

                # Post an error message
                messages.error(request, format_errors(form.errors))

        # Handle removals by deleting the membership record
        if 'id' in request.POST:

            # ID is non-user controlled, so assume it's safe
            remove_user_id = int(request.POST.get('id'))

            # Find and delete the membership record
            try:
                OrganizationMembership.objects.get(user_id=remove_user_id, organization_id=id).delete()
            except OrganizationMembership.DoesNotExist:
                raise Http404()
            organization.members -= 1
            organization.save()

    # Get a list of organization members (as users)
    users = get_users(id, 'organization')

    # Check if the member count only includes the owner
    if organization.members == 1:
        messages.info(request, 'Your organization does not have any members. Invite some!')

    # Give the template a title
    title = organization.name + ': Edit Users'

    # Render the template with the queried data set
    return render(request, 'backend/organization/manage_users.html', {
        'title': title, 'users': users, 'form': form, 'organization': organization,
    })
