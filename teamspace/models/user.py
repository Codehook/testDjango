"""
User Model

This represents details related to a user. It's based on Django's AbstractBaseUser.
"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # The authentication backend for this model
    backend = settings.AUTHENTICATION_BACKENDS[0]

    # These fields are required but may not be used
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    USERNAME_FIELD = 'username'

    # A manager is also required but may not be used
    objects = UserManager()

    # Define instance variables here
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.member_date = None

    def set_member_date(self, date):
        self.member_date = date

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
