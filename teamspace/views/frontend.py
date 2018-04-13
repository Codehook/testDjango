"""
Frontend Controller

For more information on controllers (views), see
https://docs.djangoproject.com/en/1.10/#the-view-layer

For the full list of requests and their responses, see
https://docs.djangoproject.com/en/1.10/ref/request-response/
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from teamspace.forms.user import UserLoginForm
from teamspace.forms.user import UserSignupForm
from teamspace.views.decorators import require_unauthenticated


@require_unauthenticated
def home(request):
    """
    Returns a basic view that acts as a starting point for Teamspace.

    :param request:
    :return: render, redirect
    """

    # Give the template a title
    title = 'Teamspace'

    # Render the template with the title
    return render(request, 'frontend/home.html', {'title': title})


@require_unauthenticated
def about(request):
    """
    Returns a basic view containing information about Teamspace.

    :param request:
    :return: render, redirect
    """

    # Give the template a title
    title = 'Teamspace: About'

    # Render the template with the title
    return render(request, 'frontend/about.html', {'title': title})


def logout(request):
    """
    Logs a user out even if they are not logged in, and redirects them back home.

    :param request:
    :return: redirect
    """

    user_logout(request)
    return redirect('frontend:home')


def login(request):
    """
    This simple web api logs a user in asynchronously.

    :param request:
    :return: JSON, redirect
    """

    # Only handle POST methods
    if request.method == 'POST':

        # Process the post data in the form
        form = UserLoginForm(request.POST)

        # Check if the form is valid
        if form.is_valid():

            # Fetch the user and log them in
            user = form.get_user()
            user_login(request, user)

            # Respond with a success message
            return JsonResponse({'valid': True})

        else:

            # Respond with the errors otherwise
            return JsonResponse({'valid': False, 'errors': form.errors})

    # Redirect the user back home otherwise
    return redirect('frontend:home')


def signup(request):
    """
    This simple web api creates a user asynchronously.

    :param request:
    :return: JSON, redirect
    """

    # Only handle POST methods
    if request.method == 'POST':

        # Process the post data in the form
        form = UserSignupForm(request.POST)

        # Check if the form is valid
        if form.is_valid():

            # Create the user and log them in
            user = form.save()
            user_login(request, user)

            # Respond with a success message
            return JsonResponse({'valid': True})

        else:

            # Respond with the errors otherwise
            return JsonResponse({'valid': False, 'errors': form.errors})

    # Redirect the user back home otherwise
    return redirect('frontend:home')
