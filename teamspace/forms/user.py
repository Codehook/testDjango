"""
User Forms

For more information on Forms, see
https://docs.djangoproject.com/en/1.10/topics/forms/

For more information on ModelForms, see
https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/
"""
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from teamspace.models import User
from teamspace.models import TeamMembership
from teamspace.models import OrganizationMembership


class UserLoginForm(forms.Form):
    """
    The UserLoginForm accepts an email address and password and queries the
    database for the given user. If the user is not found or the email address
    is invalid, an error will be raised.
    """

    # Users must provide an email and password
    email = forms.EmailField()
    password = forms.CharField(strip=False)

    # A list of error messages
    error_messages = {
        'invalid_login': 'Your email or password are incorrect.',
        'inactive': 'You cannot log in at this time.',
    }

    # Indicate the HTML fields
    class Meta:
        fields = ['email', 'password']

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        self.user = None
        super(UserLoginForm, self).__init__(*args, **kwargs)

    # Attempts to authenticate the user
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            else:
                self.login_allowed(self.user)
        return self.cleaned_data

    # Determines if the user can log in
    def login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

    # Returns the user
    def get_user(self):
        return self.user


class UserSignupForm(forms.ModelForm):
    """
    The UserSignupForm will create a new User given the required fields and run
    a series of validators on the fields. Errors will be raised for every
    invalid field.
    """

    # Confirm password fields
    password_one = forms.CharField(strip=False)
    password_two = forms.CharField(strip=False)

    # A list of error messages
    error_messages = {
        'password_mismatch': 'The two password fields did not match.',
    }

    # Reference the User model
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password_one', 'password_two']
        error_messages = {
            'first_name': {
                'required': 'Please enter your first name.',
            },
            'last_name': {
                'required': 'Please enter your last name.',
            },
            'username': {
                'required': 'Please enter a username.',
                'unique': 'This username is taken.',
            },
            'email': {
                'required': 'Please enter your email address.',
                'unique': 'This email address is taken.',
            },
        }

    # Make sure the passwords match
    def clean_password_two(self):
        password_one = self.cleaned_data.get('password_one')
        password_two = self.cleaned_data.get('password_two')

        # Check if the password fields match
        if password_one and password_two and password_one != password_two:
            raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')

        # Set the attributes in the model
        self.instance.first_name = self.cleaned_data.get('first_name')
        self.instance.last_name = self.cleaned_data.get('last_name')
        self.instance.username = self.cleaned_data.get('username')
        self.instance.email = self.cleaned_data.get('email')

        # Run some password validators with the model
        password_validation.validate_password(self.cleaned_data.get('password_two'), self.instance)

        # Return the validated password
        return password_two

    # Specialized save function
    def save(self, commit=True):
        user = super(UserSignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password_one'])
        if commit:
            user.save()
        return user


class AddMember(forms.Form):
    """
    The AddMember form creates a unique membership record given an email
    address and an organization or team id.
    """

    # Users must provide an email
    email = forms.EmailField()

    # A list of error messages
    error_messages = {
        'not_found': 'We couldn\'t find this user.',
        'org_member': 'This user is already a member of this organization.',
        'team_member': 'This user is already a member of this team.',
    }

    # Indicate the HTML fields
    class Meta:
        fields = ['email']

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        self.user = None
        self.id = kwargs.pop('id', 0)
        self.team = kwargs.pop('team', False)
        self.organization = kwargs.pop('organization', False)
        super(AddMember, self).__init__(*args, **kwargs)

    # Attempts to find the user
    def clean(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                self.user = User.objects.get(email__exact=email)
            except User.DoesNotExist:
                raise forms.ValidationError(self.error_messages['not_found'], code='not_found')
            if self.user:
                if self.organization:
                    try:
                        OrganizationMembership.objects.get(user_id=self.user.id, organization_id=self.id)
                        raise forms.ValidationError(self.error_messages['org_member'], code='org_member')
                    except OrganizationMembership.DoesNotExist:
                        pass
                elif self.team:
                    try:
                        TeamMembership.objects.get(user_id=self.user.id, team_id=self.id)
                        raise forms.ValidationError(self.error_messages['team_member'], code='team_member')
                    except TeamMembership.DoesNotExist:
                        pass
        return self.cleaned_data

    # Create a membership record for the user
    def add_member(self):
        if self.organization:
            OrganizationMembership.objects.create(user_id=self.user.id, organization_id=self.id)
        if self.team:
            TeamMembership.objects.create(user_id=self.user.id, team_id=self.id)
