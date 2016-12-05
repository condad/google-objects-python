# -*- coding: utf-8 -*-

import pytest

import os
import sys
import logging

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

from google_objects import SheetsAPI
from google_objects.sheets import Spreadsheet, Sheet, Block


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def client(credentials):
    return SheetsAPI(credentials)


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

        # test cell types
        for cell in block:
            assert isinstance(cell, Block.Cell)
            value = str(cell.value)
            print value
            logger.debug(type(value))
            logger.debug(value)


def test_sheets(spreadsheet):
    for sheet in spreadsheet:
        assert isinstance(sheet, Sheet)

        assert hasattr(sheet, 'properties')
        assert hasattr(sheet, 'title')
        assert hasattr(sheet, 'id')

        block = sheet.values()
        assert isinstance(block, Block)

        # test cell types
        for cell in block:
            assert isinstance(cell, Block.Cell)


def test_ranges(spreadsheet):
        for named_rng in spreadsheet.named_ranges():
            vals = named_rng.values()
            assert isinstance(vals, Block)
