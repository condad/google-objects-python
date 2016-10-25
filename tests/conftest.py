import pytest
import os

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials


GOOGLE_SERVICE_NAME = os.getenv('GOOGLE_SERVICE_NAME')
GOOGLE_SERVICE_PATH = os.getenv('GOOGLE_SERVICE_PATH')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')


def _find_credentials(name=GOOGLE_SERVICE_NAME):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, GOOGLE_SERVICE_PATH)
    credential_path = os.path.join(credential_dir, name)
    return credential_path


@pytest.fixture
def credentials(request):
    """Sets Google Service Account Credentials with
    Correct scope.
    """

    creds = _find_credentials()
    scopes = 'https://www.googleapis.com/auth/drive'

    return ServiceAccountCredentials\
        .from_json_keyfile_name(creds, scopes).create_delegated(ADMIN_EMAIL)
