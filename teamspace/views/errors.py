"""
Error Handlers
"""
from django.contrib import messages
from django.shortcuts import redirect


def handler404(request):
    if request.user.is_authenticated():
        messages.warning(request, 'The request could not be found.')
        return redirect('dashboard:home')
    else:
        return redirect('frontend:home')
