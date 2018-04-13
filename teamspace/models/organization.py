"""
Organization Model

This represents details related to an organization.
"""
from django.db import models


class Organization(models.Model):
    from teamspace.models import User

    # Database fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=50000)
    address = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=2)
    state = models.CharField(blank=True, max_length=2)
    members = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        super(Organization, self).__init__(*args, **kwargs)
        self.active_teams = []
        self.markdown = None

    # Sets a list of teams given a user id
    def set_active_teams(self, user_id):
        from teamspace.models import Team
        from teamspace.models import TeamMembership

        # Get a list of teams in this organization
        teams = Team.objects.defer('description').filter(parent_id=self.id)

        # Loop through the teams
        for team in teams:

            # Check if the membership exists and add it to the list
            if TeamMembership.objects.filter(user_id=user_id, team_id=team.id).exists():
                self.active_teams.append(team)
