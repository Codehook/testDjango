"""
Team Forms

For more information on Forms, see
https://docs.djangoproject.com/en/1.10/topics/forms/

For more information on ModelForms, see
https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
"""
from django import forms
from teamspace.models import Team
from teamspace.models import TeamMembership

FIELDS = ['name', 'description']
ERRORS = {
    'name': {
        'required': 'Please enter your team name.',
        'unique': 'This team name is taken.',
    },
    'description': {
        'required': 'Please enter a team description.',
    },
}


class TeamCreateForm(forms.ModelForm):
    """
    The TeamCreateForm will create a new team given the required fields and
    create a TeamMembership record when the form is saved and committed.
    """

    # Reference the Team model
    class Meta:
        model = Team
        fields = FIELDS
        error_messages = ERRORS

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        self.owner_id = kwargs.pop('owner_id')
        self.parent_id = kwargs.pop('parent_id')
        super(TeamCreateForm, self).__init__(*args, **kwargs)

    # Specialized save function
    def save(self, commit=True):
        team = super(TeamCreateForm, self).save(commit=False)
        team.owner_id = self.owner_id
        team.parent_id = self.parent_id
        if commit:
            team.save()
            TeamMembership.objects.create(team_id=team.id, user_id=team.owner_id)
        return team


class TeamEditForm(forms.ModelForm):
    """
    The TeamEditForm will update an existing team given an instance
    of the Team and post data if it exists. The Team will be saved
    when the form is saved.
    """

    # Reference the Team model
    class Meta:
        model = Team
        fields = FIELDS
        error_messages = ERRORS
