import sys
import logging

import pytest
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_objects.clients import DriveAPI
from google_objects.drive import File, Permission
from google_objects.utils import _find_credentials


# SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
SCOPES = 'https://www.googleapis.com/auth/drive'
USER_EMAIL = 'team@xyzfoundation.com'
FILE = '15SOeUydjJ-IGzBZxPzBmwTAkUXKuje-ciZWWddEcitY'


@pytest.fixture
def credentials():
    creds = _find_credentials()
    return ServiceAccountCredentials \
        .from_json_keyfile_name(creds, SCOPES).create_delegated(USER_EMAIL)


@pytest.fixture
def client(credentials):
    return DriveAPI(credentials)


def test_get_file(client):
    with client.get_file(FILE) as test_file:
        assert isinstance(test_file, File)

        permission = test_file.new_permission()
        assert isinstance(permission, Permission)

        permission.email = 'sully4792@gmail.com'
        permission.role = 'commenter'
        permission.type = 'user'
        print permission.as_dict()
    # asser
    # for permission in permissions:
    #     assert isinstance(permission, Permission)
