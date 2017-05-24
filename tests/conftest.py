import pytest
import os

GOOGLE_SERVICE_NAME = os.getenv('GOOGLE_CREDENTIALS')
GOOGLE_SERVICE_PATH = os.getenv('GOOGLE_SERVICE_PATH')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')


def _find_credentials(name=GOOGLE_SERVICE_NAME):
    return os.path.expanduser(GOOGLE_SERVICE_NAME)


@pytest.fixture
def credentials(request):
    """Sets Google Service Account Credentials with
    Correct scope.
    """

    creds = _find_credentials()
    scope = ['drive']

    return (creds, scope, ADMIN_EMAIL)
