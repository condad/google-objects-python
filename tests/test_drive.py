# -*- coding: utf-8 -*-

import pytest
import os

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_objects import DriveAPI
from google_objects.drive import File, Permission


@pytest.fixture
def client(credentials):
    return DriveAPI(credentials)


def test_file_list(client):
    assert client.list_files()
    assert client.list_files('folder')
    assert client.list_files('document')


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

    assert hasattr(permission, 'id')
    assert hasattr(permission, 'email')
    assert hasattr(permission, 'role')
    assert hasattr(permission, 'type')
