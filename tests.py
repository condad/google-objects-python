import sys

import pytest
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from client import Client, _find_credentials
from models import Presentation, Page


SCOPES = 'https://www.googleapis.com/auth/drive'
USER_EMAIL = 'team@xyzfoundation.com'
API_KEY = 'AIzaSyBe7-2oJUa_Gyl4SdDdPfLRymCKCdeb0zU'


@pytest.fixture
def credentials():
    creds = _find_credentials()
    return ServiceAccountCredentials.from_json_keyfile_name(creds, SCOPES).create_delegated(USER_EMAIL)

def test_client(credentials):
    """TODO: Docstring for test_client.

    :credentials: TODO
    :returns: TODO

    """
    client = Client()
