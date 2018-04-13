"""
Message Forms

For more information on Forms, see
https://docs.djangoproject.com/en/1.10/topics/forms/

For more information on ModelForms, see
https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
"""
from django import forms
from teamspace.models import Message


class MessageCreateForm(forms.ModelForm):
    """
    The MessageCreateForm will create a new message given a team and user.
    """

    # Reference the Message model
    class Meta:
        model = Message
        fields = ['message']

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        self.owner_id = kwargs.pop('owner_id')
        self.parent_id = kwargs.pop('parent_id')
        super(MessageCreateForm, self).__init__(*args, **kwargs)

    # Specialized save function
    def save(self, commit=True):
        message = super(MessageCreateForm, self).save(commit=False)
        message.owner_id = self.owner_id
        message.parent_id = self.parent_id
        if commit:
            message.save()
        return message
