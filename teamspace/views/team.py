"""
Team Controller

For more information on controllers (views), see
https://docs.djangoproject.com/en/1.10/#the-view-layer

For the full list of requests and their responses, see
https://docs.djangoproject.com/en/1.10/ref/request-response/
"""
import os
from django.views.static import serve
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from teamspace.utils import get_users
from teamspace.utils import get_files
from teamspace.utils import get_events
from teamspace.utils import get_messages
from teamspace.utils import format_errors
from teamspace.utils import format_description
from teamspace.models import File
from teamspace.models import Team
from teamspace.models import TeamMembership
from teamspace.models import Organization
from teamspace.forms.user import AddMember
from teamspace.forms.team import TeamEditForm
from teamspace.forms.event import EventCreateForm
from teamspace.forms.message import MessageCreateForm
from teamspace.views.decorators import require_team_owner
from teamspace.views.decorators import require_team_member
from teamspace.views.decorators import require_authenticated


@require_authenticated
@require_team_member
def leave(request, id):
    """
    Deletes the membership record of the queried team if the user is a member.

    :param request:
    :param id: Team ID
    :return: redirect
    """

    # Fetch the corresponding team
    try:
        team = Team.objects.get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Fetch the parent organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()

    # Fetch the corresponding team membership
    try:
        membership = TeamMembership.objects.get(user_id=request.user.id, team_id=team.id)
    except TeamMembership.DoesNotExist:
        raise Http404()

    # Delete the membership and decrement the member count
    if membership:
        membership.delete()
        team.members -= 1
        team.save()
        messages.info(request, 'You have left the team.')

    # Redirect the user back to the team view
    return redirect('organization:team:view', organization.id)


@require_authenticated
@require_team_owner
def delete(request, id):
    """
    Deletes the queried team if the user is the owner.

    :param request:
    :param id: Team ID
    :return: redirect
    """

    # Fetch the corresponding team
    try:
        team = Team.objects.get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Fetch the parent organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()

    # Make sure the user is the owner
    if team.owner_id == request.user.id:
        team.delete()
        messages.info(request, 'The team has been deleted.')

    # Redirect the user back to the team view
    return redirect('organization:team:view', organization.id)


@require_authenticated
@require_team_member
def home(request, id):
    """
    Returns a view with the queried team and a parsed markdown description.

    :param request:
    :param id: Team ID
    :return: render
    """

    # Fetch the corresponding team
    try:
        team = Team.objects.get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Parse the description
    team.markdown = format_description(team.description)

    # Fetch the parent organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()

    # Give the template a title
    title = team.name + ': About'

    # Render the template with the queried data set
    return render(request, 'backend/team/home.html', {
        'title': title, 'team': team, 'organization': organization,
    })


@require_authenticated
@require_team_member
def events(request, id):
    """
    Returns a view with the queried team and a list of events.

    :param request:
    :param id: Team ID
    :return: render
    """

    # Fetch the corresponding team
    try:
        team = Team.objects.defer('description').get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Fetch the parent organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()

    # Give the template a title
    title = team.name + ': Events'

    # Initialize the form
    form = None

    # Handle post methods
    if request.method == 'POST':

        # Process the post data in the form
        form = EventCreateForm(request.POST, owner_id=request.user.id, parent_id=team.id)

        # Check if the form is valid and create the message
        if form.is_valid():
            form.save()
            form = None

        # Post an error message
        else:
            messages.error(request, format_errors(form.errors))

    # Fetch the event list
    events = get_events(team.id)

    # Post a message if empty
    if not events:
        messages.info(request, 'There are no events to display.')

    # Render the template with the queried data set
    return render(request, 'backend/team/events.html', {
        'title': title, 'team': team, 'organization': organization,
        'form': form, 'events': events,
    })


@require_authenticated
@require_team_member
def files(request, id):
    """
    Returns a view with a file manager window in the queried team.

    :param request:
    :param id: Team ID
    :return: render
    """
    from teamspace import settings

    if request.method == 'GET':
        if request.GET.get('file_id'):
            try:
                # This does not scale well, but it'll work for a presentation
                fid = int(request.GET.get('file_id'))
                file = File.objects.get(pk=fid)
                if file.parent_id == int(id):
                    return serve(request, os.path.basename(file.location), os.path.dirname(file.location))
                else:
                    messages.error(request, 'This file could not be found.')
            except ValueError:
                messages.error(request, 'Invalid file ID.')

    # Fetch the corresponding team
    try:
        team = Team.objects.defer('description').get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Fetch the parent organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()

    # Give the template a title
    title = team.name + ': Files'

    # Upload the requested file
    if request.method == 'POST':
        from teamspace.views.google import authorize
        google_request = {'team_id': team.id, 'file_id': request.POST.get('file_id')}
        return redirect(authorize(request, google_request))

    # Fetch the file list
    files = get_files(team.id)

    # Post a message if empty
    if not files:
        messages.info(request, 'There are no files to display. Share some!')

    # Render the template with the queried data set
    return render(request, 'backend/team/files.html', {
        'title': title, 'team': team,
        'organization': organization, 'files': files,
        'app_id': settings.PROVIDERS.get('GOOGLE').get('ID'),
        'api_key': settings.PROVIDERS.get('GOOGLE').get('APIKEY'),
        'client_id': settings.PROVIDERS.get('GOOGLE').get('CLIENT'),
    })


@require_authenticated
@require_team_member
def chat(request, id):
    """
    Returns a view with a chat window for the queried team.

    :param request:
    :param id: Team ID
    :return: render
    """

    # Fetch the corresponding team
    try:
        team = Team.objects.defer('description').get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Fetch the parent organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()

    # Give the template a title
    title = team.name + ': Chat'

    # Initialize the form
    form = None

    # Handle post methods
    if request.method == 'POST':

        # Process the post data in the form
        form = MessageCreateForm(request.POST, owner_id=request.user.id, parent_id=team.id)

        # Check if the form is valid and create the message
        if form.is_valid():
            form.save()
            form = None

        # Post an error message
        else:
            messages.error(request, 'Your message could not be posted.')

    # Fetch the message list
    team_messages = get_messages(team.id)

    # Post a message if empty
    if not team_messages:
        messages.info(request, 'There are no messages to display.')

    # Render the template with the queried data set
    return render(request, 'backend/team/chat.html', {
        'title': title, 'team': team, 'organization': organization,
        'form': form, 'team_messages': team_messages,
    })


@require_authenticated
@require_team_member
def users(request, id):
    """
    Returns a view with a list of members in the queried team.

    :param request:
    :param id: Team ID
    :return: render
    """

    # Fetch the corresponding team
    try:
        team = Team.objects.defer('description').get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Fetch a list of team members
    users = get_users(id, 'team')

    # Fetch the parent organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()

    # Give the template a title
    title = team.name + ': Users'

    # Render the template with the queried data set
    return render(request, 'backend/team/users.html', {
        'title': title, 'team': team, 'users': users, 'organization': organization,
    })


@require_authenticated
@require_team_owner
def manage_edit(request, id):
    """
    Returns a view where an owner can edit their team.

    :param request:
    :param id: Team ID
    :return: render
    """

    # Fetch the corresponding team
    try:
        team = Team.objects.defer('description').get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Fetch the parent organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()

    # Give the template a title
    title = team.name + ': Edit'

    # Handle a POST method
    if request.method == 'POST':

        # Update the form with the post data
        form = TeamEditForm(request.POST, instance=team)

        # Check if the form is valid
        if form.is_valid():

            # Update and save the team
            form.save()

            # Post a success message
            messages.success(request, 'Settings successfully saved.')

        else:

            # Post an error message
            messages.error(request, format_errors(form.errors))

    else:

        # Give the default form
        form = TeamEditForm(instance=team)

    # Render the template with the queried data set
    return render(request, 'backend/team/manage_edit.html', {
        'title': title, 'form': form, 'team': team, 'organization': organization,
    })


@require_authenticated
@require_team_owner
def manage_users(request, id):
    """
    Returns a view with a list of users and a form to add users.

    :param request:
    :param id: Team ID
    :return: render
    """

    # Fetch the corresponding team
    try:
        team = Team.objects.defer('description').get(pk=id)
    except Team.DoesNotExist:
        raise Http404()

    # Fetch the corresponding organization
    try:
        organization = Organization.objects.defer('description', 'address', 'country', 'state').get(pk=team.parent_id)
    except Organization.DoesNotExist:
        raise Http404()
    form = None

    # Handle a POST method
    if request.method == 'POST':

        # Handle invitations by creating a membership record
        if 'email' in request.POST:

            # Process the email address
            form = AddMember(request.POST, id=id, team=True)

            # Check if the form is valid
            if form.is_valid():

                # Create the membership record
                form.add_member()
                team.members += 1
                team.save()
                form = None

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
                TeamMembership.objects.get(user_id=remove_user_id, team_id=id).delete()
            except TeamMembership.DoesNotExist:
                raise Http404()
            team.members -= 1
            team.save()

    # Get a list of team members (as users)
    users = get_users(id, 'team')

    # Check if the member count only includes the owner
    if team.members == 1:
        messages.info(request, 'Your team does not have any members. Invite some!')

    # Give the template a title
    title = team.name + ': Edit Users'

    # Render the template with the queried data set
    return render(request, 'backend/team/manage_users.html', {
        'title': title, 'users': users, 'form': form, 'team': team, 'organization': organization,
    })
