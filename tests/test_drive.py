# -*- coding: utf-8 -*-

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


@pytest.fixture
def drive_file(client):
    return client.get_file(FILE)


def test_file(drive_file):
    assert isinstance(drive_file, File)

    # test properties
    assert hasattr(drive_file, 'id')
    assert hasattr(drive_file, 'type')


def test_permissions(drive_file):
    permission = drive_file.create(
        email='sully4792@gmail.com',
        role='commenter',
        type='user',
    )

    # test properties
    assert hasattr(permission, 'id')
    assert hasattr(permission, 'email')
    assert hasattr(permission, 'role')
    assert hasattr(permission, 'type')
