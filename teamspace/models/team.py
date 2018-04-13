"""
Team Model

This represents details related to a team.
"""
from django.db import models


class Team(models.Model):
    from teamspace.models import User
    from teamspace.models import Organization

    # Database fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=50000)
    members = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        super(Team, self).__init__(*args, **kwargs)
        self.markdown = None
