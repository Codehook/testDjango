"""
Dashboard Controller

For more information on controllers (views), see
https://docs.djangoproject.com/en/1.10/#the-view-layer

For the full list of requests and their responses, see
https://docs.djangoproject.com/en/1.10/ref/request-response/
"""
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from teamspace.utils import format_errors
from teamspace.models import Organization
from teamspace.models import OrganizationMembership
from teamspace.forms.organization import OrganizationCreateForm
from teamspace.views.decorators import require_authenticated


@require_authenticated
def home(request):
    """
    Returns a view that acts as a starting point for the user.

    :param request:
    :return: render, redirect
    """

    # Give the template a title
    title = 'Dashboard: Home'

    # Render the template with the queried data set
    return render(request, 'backend/dashboard/home.html', {'title': title})


@require_authenticated
def user_edit(request):
    """
    Returns a view with a form for the user to edit their account.

    :param request:
    :return: render, redirect
    """

    # Give the template a title
    title = 'Dashboard: Edit Account'

    # Render the template with the queried data set
    return render(request, 'backend/dashboard/user_edit.html', {'title': title})


@require_authenticated
def user_password(request):
    """
    Returns a view with a form for the user to change their password.

    :param request:
    :return: render, redirect
    """

    # Give the template a title
    title = 'Dashboard: Change Password'

    # Render the template with the queried data set
    return render(request, 'backend/dashboard/user_password.html', {'title': title})


@require_authenticated
def orgs_view(request):
    """
    Returns a view containing a list of organizations the user is a member of.

    :param request:
    :return: render, redirect
    """

    # Get the list of organizations where the user is a member
    memberships = OrganizationMembership.objects.filter(user_id=request.user.id)
    organizations = []

    # Fetch each organization given a membership
    for membership in memberships:
        organizations.append(Organization.objects.defer('description', 'address', 'country', 'state').get(pk=membership.organization_id))

    # Fetch a list of active teams for each organization
    for organization in organizations:
        organization.set_active_teams(request.user.id)

    # Flash a message if the list of teams is empty
    if not organizations:
        messages.info(request, 'You\'re not a member of any organization yet. Go create one!')

    # Give the template a title
    title = 'Dashboard: View Organizations'

    # Render the template with the queried data set
    return render(request, 'backend/dashboard/organizations_view.html', {
        'title': title, 'organizations': organizations,
    })


@require_authenticated
def orgs_create(request):
    """
    Returns a view where users can create an organization.

    :param request:
    :return: render, redirect
    """

    # Give the template a title
    title = 'Dashboard: Create Organization'

    # Handle a POST method
    if request.method == 'POST':

        # Process the post data in the form
        form = OrganizationCreateForm(request.POST, owner_id=request.user.id)

        # Check if the form is valid
        if form.is_valid():

            # Create the organization
            organization = form.save()

            # Post a success message
            messages.success(request, 'Organization successfully created.')

            # Redirect to the newly created team
            return redirect('organization:home', organization.id)

        else:

            # Post an error message
            messages.error(request, format_errors(form.errors))

            # Return with the errors otherwise
            return render(request, 'backend/dashboard/organizations_create.html', {
                'title': title, 'form': form,
            })

    # Render the creation template
    return render(request, 'backend/dashboard/organizations_create.html', {'title': title})
