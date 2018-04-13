"""
File Model

This represents details related to a team file.
"""
from django.db import models


class File(models.Model):
    from teamspace.models import User
    from teamspace.models import Team

    # Database fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=255)
    location = models.CharField(blank=False, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
        self.user = None
