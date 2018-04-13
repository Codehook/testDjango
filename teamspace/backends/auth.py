"""
User Authentication

For more information on authenticating users, see
https://docs.djangoproject.com/en/1.10/topics/auth/default/#authenticating-users
"""
from django.contrib.auth.backends import ModelBackend
from teamspace.models import User


class UserModelBackend(ModelBackend):
    """
    The UserModelBackend creates an additional authenticator that allows users
    to log in with an email address instead of a username. The email address
    will be queried for in the database and the password will be verified.
    """

    # Custom authenticator using an email address
    def authenticate(self, email='', password='', **kwargs):
        try:
            user = User.objects.get(email__exact=email)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
