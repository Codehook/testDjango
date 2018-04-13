"""
Organization Membership Model

This represents a membership between a user and an organization.
"""
from django.db import models


class OrganizationMembership(models.Model):
    from teamspace.models import User
    from teamspace.models import Organization

    # Database fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
