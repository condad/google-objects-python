import pytest
import os

from oauth2client.service_account import ServiceAccountCredentials


ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
AUTH_SCOPES = (
    'https://www.googleapis.com/auth/drive',
    # 'https://www.googleapis.com/auth/spreadsheets,
    # 'https://www.googleapis.com/auth/presentations',
)


@pytest.fixture
def credentials(request):
    """Sets Google Service Account Credentials with
    Correct scope.
    """

    creds = os.path.expanduser(GOOGLE_CREDENTIALS)
    return ServiceAccountCredentials\
        .from_json_keyfile_name(creds, AUTH_SCOPES).create_delegated(ADMIN_EMAIL)
