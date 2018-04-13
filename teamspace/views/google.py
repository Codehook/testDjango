import os
import json
import httplib2

from apiclient import http
from apiclient import errors
from apiclient import discovery
from oauth2client import client
from django.http import Http404
from django.shortcuts import redirect
from django.core.cache import cache
from teamspace.models.file import File
from teamspace.views.decorators import require_authenticated

CLIENT_SECRET_FILE = 'config/google.json'
REDIRECT_URI = 'http://localhost:8000/providers/google'
SCOPES = 'https://www.googleapis.com/auth/drive'


def create_file(service, file_id, team_id):
    """
    This will create a file on the file system: ./.team_uploads/{{team.id}}/{{file_name}}

    :param service:
    :param file_id:
    :param team_id:
    :return:
    """
    try:
        file_details = service.files().get(fileId=file_id).execute()
    except errors.HttpError as error:
        #print('An error occurred: %s' % error)
        pass
    file_name = file_details.get('name')
    team_dir = os.path.join(os.getcwd(), '.team_uploads', str(team_id))
    if not os.path.exists(team_dir):
        os.makedirs(team_dir)
    file_path = os.path.join(team_dir, file_name)
    return open(file_path, 'wb')


def download_file(service, file_id, local_fd):
    """
    This will actually download the file from Google Drive.

    :param service:
    :param file_id:
    :param local_fd:
    :return:
    """
    download_progress = None
    request = service.files().get_media(fileId=file_id)
    media_request = http.MediaIoBaseDownload(local_fd, request)
    while True:
        try:
            download_progress, done = media_request.next_chunk()
        except errors.HttpError as error:
            #print('An error occurred: %s' % error)
            break
        if download_progress:
            #print('Download Progress: %d%%' % int(download_progress.progress() * 100))
            pass
        if done:
            #print('Download Complete')
            pass
    if download_progress and download_progress.progress() >= 1.0:
        return True


def authorize(request, google_request):
    """
    This will redirect the user to authorize the application and cache some details about the file.

    :param request:
    :param google_request:
    :return:
    """
    # Cache the request
    cache.set('user#' + str(request.user.id), json.dumps(google_request))
    # Return the redirect uri
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    return flow.step1_get_authorize_url(redirect_uri=REDIRECT_URI)


def upload(request, code):
    """
    This will authorize the application and fetch some cached details about the file to upload to the server.

    :param request:
    :param code:
    :return:
    """
    # Create Google service
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.step1_get_authorize_url(redirect_uri=REDIRECT_URI)

    # Restore the request from the cache
    google_request = json.loads(cache.get('user#' + str(request.user.id)))

    # Authorize with the service
    credentials = flow.step2_exchange(code)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # Create the local file by name
    file_id = google_request.get('file_id')
    team_id = google_request.get('team_id')
    local_fd = create_file(service, file_id, team_id)

    # Download the file and close it
    if download_file(service, file_id, local_fd):
        location = os.path.abspath(local_fd.name)
        name = os.path.basename(local_fd.name)
        File.objects.create(owner_id=request.user.id, parent_id=team_id, name=name, location=location)
    local_fd.close()

    # Return the team id
    return team_id


@require_authenticated
def index(request):
    """
    This will process OAuth connections with Google.

    :param request:
    :return:
    """
    # Download the file from Google
    if request.method == 'GET':
        if request.GET.get('code'):
            code = request.GET.get('code')
            team_id = upload(request, code)
            return redirect('team:files', team_id)
    if request.method == 'POST':
        pass
    raise Http404()
