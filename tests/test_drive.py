# -*- coding: utf-8 -*-

import pytest
import os

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_objects.clients import DriveAPI
from google_objects.drive import File, Permission


@pytest.fixture
def credentials():
    creds = os.path.expanduser(os.getenv('GOOGLE_CREDENTIALS'))
    user_email = os.getenv('GOOGLE_EMAIL')
    scope = os.getenv('DRIVE_SCOPE')

    return ServiceAccountCredentials\
        .from_json_keyfile_name(creds, scope).create_delegated(user_email)


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
