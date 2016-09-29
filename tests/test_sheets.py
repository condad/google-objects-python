import sys
import logging

import pytest
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_objects.clients import SheetsAPI, _find_credentials
from google_objects.sheets import Spreadsheet, Block


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
USER_EMAIL = 'team@xyzfoundation.com'
SPREADSHEET = '1k-P5NUVAO2c8pXXuKJ4ctCyko_WlL4bF55H_R6ZXhLY'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def credentials():
    creds = _find_credentials()
    return ServiceAccountCredentials \
        .from_json_keyfile_name(creds, SCOPES).create_delegated(USER_EMAIL)


@pytest.fixture
def client(credentials):
    return SheetsAPI(credentials)


def test_get_spreadsheet(client):
    spreadsheet = client.get_spreadsheet(SPREADSHEET)
    assert isinstance(spreadsheet, Spreadsheet)

    # test blocks
    for i, sheet in enumerate(spreadsheet):
        block = sheet.get_values()
        assert isinstance(block, Block)

        # test cell types
        for row in block:
            for cell in row:
                assert isinstance(cell, Block.Cell)
                value = str(cell.value)
                logger.debug(type(value))
                logger.debug(value)
