"""
Organization Forms

For more information on Forms, see
https://docs.djangoproject.com/en/1.10/topics/forms/

For more information on ModelForms, see
https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
"""
from django import forms
from teamspace.models import Organization
from teamspace.models import OrganizationMembership

FIELDS = ['name', 'description', 'address', 'country', 'state']
ERRORS = {
    'name': {
        'required': 'Please enter the name of your organization.',
        'unique': 'This organization name is taken.',
    },
    'description': {
        'required': 'Please enter an organization description.',
    },
}


class OrganizationCreateForm(forms.ModelForm):
    """
    The OrganizationCreateForm will create a new organization given the
    required fields and create an OrganizationMembership record when the form
    is saved and committed.
    """

    # Reference the Organization model
    class Meta:
        model = Organization
        fields = FIELDS
        error_messages = ERRORS

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        self.owner_id = kwargs.pop('owner_id')
        super(OrganizationCreateForm, self).__init__(*args, **kwargs)

    # Specialized save function
    def save(self, commit=True):
        organization = super(OrganizationCreateForm, self).save(commit=False)
        organization.owner_id = self.owner_id
        if commit:
            organization.save()
            OrganizationMembership.objects.create(organization_id=organization.id, user_id=organization.owner_id)
        return organization


class OrganizationEditForm(forms.ModelForm):
    """
    The OrganizationEditForm will update an existing organization given an instance
    of the Organization and post data if it exists. The Organization will be saved
    when the form is saved.
    """

    # Reference the Organization model
    class Meta:
        model = Organization
        fields = FIELDS
        error_messages = ERRORS
