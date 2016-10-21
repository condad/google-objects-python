import os
import sys

import pytest
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_objects import SlidesAPI
from google_objects.utils import find_credentials
from google_objects.slides import Presentation, Page


SCOPES = os.getenv('SLIDES_SCOPE')
USER_EMAIL = os.getenv('USER_EMAIL')
API_KEY = os.getenv('API_KEY')
PRESENTATION = os.getenv('PRESENTATION')
PAGE = os.getenv('PAGE')
REGEX = os.getenv('REGEX')


@pytest.fixture
def credentials():
    creds = find_credentials()
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


# def test_get_matches(client):
#     presentation = client.get_presentation(PRESENTATION)

#     with presentation:
#         tags = presentation.get_matches(REGEX)
#         # print len(tags) + 'tags'
#         for i, tag in enumerate(tags):
#             presentation.replace_text(tag, i)
