"""
Team Membership Model

This represents a membership between a user and a team.
"""
from django.db import models


class TeamMembership(models.Model):
    from teamspace.models import User
    from teamspace.models import Team

    # Database fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
