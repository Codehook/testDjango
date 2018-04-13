"""
Event Forms

For more information on Forms, see
https://docs.djangoproject.com/en/1.10/topics/forms/

For more information on ModelForms, see
https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
"""
from django import forms
from teamspace.models import Event


class EventCreateForm(forms.ModelForm):
    """
    The EventCreateForm will create a new message given a team and user.
    """

    # Reference the Message model
    class Meta:
        model = Event
        fields = ['title', 'description', 'start', 'end']
        error_messages = {
            'title': {
                'required': 'Please enter a title.',
            },
            'description': {
                'required': 'Please enter a short description.',
            },
        }

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        self.owner_id = kwargs.pop('owner_id')
        self.parent_id = kwargs.pop('parent_id')
        super(EventCreateForm, self).__init__(*args, **kwargs)

    # Specialized save function
    def save(self, commit=True):
        event = super(EventCreateForm, self).save(commit=False)
        event.owner_id = self.owner_id
        event.parent_id = self.parent_id
        if commit:
            event.save()
        return event
