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
PAGE = '' # TODO
REGEX = r'{{.*?}}'


@pytest.fixture
def credentials():
    creds = _find_credentials()
    return ServiceAccountCredentials \
        .from_json_keyfile_name(creds, SCOPES).create_delegated(USER_EMAIL)


def test_get_presentation(credentials):
    client = Client(credentials, API_KEY)
    presentation = client.get_presentation(PRESENTATION)
    assert type(presentation) is Presentation


def test_get_page(credentials):
    client = Client(credentials, API_KEY)
    page = client.get_page(PRESENTATION, PAGE)
    assert type(page) is Page


def test_get_matches(credentials):
    client = Client(credentials, API_KEY)
    presentation = client.get_presentation(PRESENTATION)

    with presentation as pres:
        tags = presentation.get_matches(REGEX)
        for tag in tags:
            pres.replace_text(tag, 'HERE')
