import sys

import pytest
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_sliders.client import Client, _find_credentials
from google_sliders.models import Presentation, Page


SCOPES = 'https://www.googleapis.com/auth/drive'
USER_EMAIL = 'team@xyzfoundation.com'
API_KEY = 'AIzaSyBe7-2oJUa_Gyl4SdDdPfLRymCKCdeb0zU'
PRESENTATION = '1gzVpBuzdrX58cKbTemnQWhgBrbd7QzFmnMen6GI8pNs'
REGEX = r'{{.*?}}'


@pytest.fixture
def credentials():
    creds = _find_credentials()
    return ServiceAccountCredentials.from_json_keyfile_name(creds, SCOPES).create_delegated(USER_EMAIL)

def test_presentation(credentials):
    client = Client(credentials, API_KEY)
    presentation = client.get_presentation(PRESENTATION)

    with presentation as pres:
        tags = presentation.find_tags(REGEX)
        for tag in tags:
            print tag
            pres.replace_text(tag, 'HERE')
        assert tags
