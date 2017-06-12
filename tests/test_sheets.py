# -*- coding: utf-8 -*-

import pytest

import os
import logging

from google_objects import SheetsClient
from google_objects.sheets.core import Spreadsheet, Sheet, Block

log = logging.getLogger(__name__)


@pytest.fixture
def client(credentials):
    return SheetsClient.from_service_account(*credentials)


@pytest.fixture
def spreadsheet(client):
    sheet_id = os.getenv('TEST_SHEET')
    return client.get_spreadsheet(sheet_id)


def test_spreadsheet(spreadsheet):
    assert isinstance(spreadsheet, Spreadsheet)

    assert hasattr(spreadsheet, 'id')
    assert hasattr(spreadsheet, 'title')

    # test blocks
    for sheet in spreadsheet:
        assert isinstance(sheet, Sheet)
        assert hasattr(sheet, 'properties')
        assert hasattr(sheet, 'title')
        assert hasattr(sheet, 'id')

        block = sheet.values()
        assert isinstance(block, Block)


def test_sheets(spreadsheet):
    for sheet in spreadsheet:
        assert isinstance(sheet, Sheet)

        assert hasattr(sheet, 'properties')
        assert hasattr(sheet, 'title')
        assert hasattr(sheet, 'id')

        block = sheet.values()
        assert isinstance(block, Block)

        # test rows
        for row in block.rows:
            assert hasattr(row, '__iter__')
