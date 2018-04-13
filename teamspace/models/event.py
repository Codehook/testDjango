"""
Event Model

This represents details related to a team event.
"""
from django.db import models


class Event(models.Model):
    from teamspace.models import User
    from teamspace.models import Team

    # Database fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Team, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=255)
    description = models.CharField(blank=False, max_length=255)
    start = models.DateField()
    end = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.user = None
