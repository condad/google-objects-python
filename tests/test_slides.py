import sys

import pytest
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_objects.clients import SlidesAPI, _find_credentials
from google_objects.slides import Presentation, Page


SCOPES = 'https://www.googleapis.com/auth/drive'
USER_EMAIL = 'team@xyzfoundation.com'
API_KEY = 'AIzaSyBe7-2oJUa_Gyl4SdDdPfLRymCKCdeb0zU'
PRESENTATION = '1gzVpBuzdrX58cKbTemnQWhgBrbd7QzFmnMen6GI8pNs'
PAGE = 'g11754963ba_0_5'
REGEX = r'{{.*?}}'


@pytest.fixture
def credentials():
    creds = _find_credentials()
    return ServiceAccountCredentials \
        .from_json_keyfile_name(creds, SCOPES).create_delegated(USER_EMAIL)


@pytest.fixture
def client(credentials):
    api = SlidesAPI(credentials, API_KEY)
    return api


def test_get_presentation(client):
    presentation = client.get_presentation(PRESENTATION)
    assert isinstance(presentation, Presentation)


def test_get_page(client):
    page = client.get_page(PRESENTATION, PAGE)
    assert isinstance(page, Page)
    assert page.read_only


def test_get_matches(client):
    presentation = client.get_presentation(PRESENTATION)

    with presentation:
        tags = presentation.get_matches(REGEX)
        # print len(tags) + 'tags'
        for i, tag in enumerate(tags):
            presentation.replace_text(tag, i)
