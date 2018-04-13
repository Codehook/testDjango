"""
Teamspace Utilities

Functionality used by more than one view should be placed here.
"""
import re
import markdown
from django.utils.html import strip_tags
from teamspace.models import User
from teamspace.models import File
from teamspace.models import Event
from teamspace.models import Message
from teamspace.models import TeamMembership
from teamspace.models import OrganizationMembership


def format_description(string):
    """
    Parses a markdown formatted description into HTML.

    :param string:
    :return string:
    """
    string = markdown.markdown(strip_tags(string), output_format='html5')
    string = re.sub(r'<blockquote>', '<blockquote class="ui segment">', string)
    string = re.sub(r'<code>', '<code class="ui tertiary segment">', string)
    return string


def format_errors(errors):
    """
    Formats a dictionary of form errors as an HTML unordered list.

    :param errors:
    :return string:
    """
    string = '<ul class="list">'
    for field in errors:
        string += '<li>' + strip_tags(errors[field]) + '</li>'
    string += '</ul>'
    return string


def get_users(id, scope):
    """
    Returns a list of members (as users) given an organization or team id.

    :param id: Organization or Team ID
    :return: users
    """

    # Fetch a list of organization members
    if scope == 'organization':
        members = OrganizationMembership.objects.filter(organization_id=id)
    elif scope == 'team':
        members = TeamMembership.objects.filter(team_id=id)
    users = []

    # Fetch the actual list of users
    for member in members:
        try:
            user = User.objects.defer('email', 'password').get(pk=member.user_id)
            user.set_member_date(member.created)
            users.append(user)
        except User.DoesNotExist:
            pass
    return users


def get_messages(id):
    """
    Returns a list of messages given a team id.

    :param id: Team ID
    :return: messages
    """

    # Fetch a list of messages and get each user
    messages = Message.objects.filter(parent_id=id).order_by('-created')
    for message in messages:
        try:
            message.user = User.objects.defer('email', 'password').get(pk=message.owner_id)
        except User.DoesNotExist:
            pass
    return messages


def get_events(id):
    """
    Returns a list of events given a team id.

    :param id: Team ID
    :return: messages
    """

    # Fetch a list of events and get each user
    events = Event.objects.filter(parent_id=id).order_by('-start')
    for event in events:
        try:
            event.user = User.objects.defer('email', 'password').get(pk=event.owner_id)
        except User.DoesNotExist:
            pass
    return events


def get_files(id):
    """
    Returns a list of files given a team id.

    :param id: Team ID
    :return: messages
    """

    # Fetch a list of events and get each user
    files = File.objects.filter(parent_id=id).order_by('-created')
    for file in files:
        try:
            file.user = User.objects.defer('email', 'password').get(pk=file.owner_id)
        except User.DoesNotExist:
            pass
    return files
