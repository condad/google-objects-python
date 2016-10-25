# -*- coding: utf-8 -*-

import pytest
import os

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_objects import DriveAPI
from google_objects.drive import File, Permission



# def _find_credentials(name='xyz_creds.json'):
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, 'lab/google-objects/.credentials')
#     credential_path = os.path.join(credential_dir, name)
#     return credential_path


# SCOPES = 'https://www.googleapis.com/auth/drive'
# USER_EMAIL = 'team@xyzfoundation.com'
# FILE = '15SOeUydjJ-IGzBZxPzBmwTAkUXKuje-ciZWWddEcitY'


# @pytest.fixture
# def credentials():
#     creds = _find_credentials()
#     return ServiceAccountCredentials \
#         .from_json_keyfile_name(creds, SCOPES).create_delegated(USER_EMAIL)


@pytest.fixture
def client(credentials):
    return DriveAPI(credentials)


@pytest.fixture
def drive_file(client):
    test_file_id = os.getenv('TEST_FILE')
    return client.get_file(test_file_id)


def test_file(drive_file):
    assert isinstance(drive_file, File)

    # test properties
    assert hasattr(drive_file, 'id')
    assert hasattr(drive_file, 'type')


def test_permissions(drive_file):
    permission = drive_file.add_permission(
        email='sully4792@gmail.com',
        role='commenter',
        type='user',
    )

    # test properties
    print 'as dict:'
    print permission.__dict__

    assert hasattr(permission, 'id')
    assert hasattr(permission, 'email')
    assert hasattr(permission, 'role')
    assert hasattr(permission, 'type')
