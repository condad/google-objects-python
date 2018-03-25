import unittest
from unittest import mock

import pandas

from tests.utils import get_data
from google_objects.sheets import SheetsClient
from google_objects.sheets import Spreadsheet
from google_objects.sheets import Sheet
from google_objects.sheets import Block

# load google sheets dummy data
spreadsheet = get_data('spreadsheet')
values = get_data('range')

# initialize mock google-api-python-client resource object
mock_resource = mock.Mock()
mock_resource.spreadsheets().get().execute.return_value = spreadsheet
mock_resource.spreadsheets().values().get().execute.return_value = values


class TestSheets(unittest.TestCase):
    """Test Google Sheets objects"""

    def setUp(self):
        self.client = SheetsClient(mock_resource)

    def test_spreadsheets(self):
        spreadsheet = self.client.get_spreadsheet('abc123')
        self.assertIsInstance(spreadsheet, Spreadsheet)

        # test spreadsheet properties
        self.assertEqual(spreadsheet.title, 'Test Google Spreadsheet')
        self.assertEqual(spreadsheet.id, 'abc123')

    def test_sheets(self):
        spreadsheet = self.client.get_spreadsheet('abc123')
        sheets = spreadsheet.sheets()
        self.assertIsInstance(sheets, list)

        for i, sheet in enumerate(sheets):
            self.assertIsInstance(sheet, Sheet)

        # test sheet properties
        first_sheet = sheets[0]
        self.assertEqual(first_sheet.title, 'First Sheet')
        self.assertEqual(first_sheet.id, 1234)

    def test_values(self):
        spreadsheet = self.client.get_spreadsheet('abc123')
        sheets = spreadsheet.sheets()
        values = sheets[0].values()
        self.assertIsInstance(values, Block)

        for row in values:
            self.assertIsInstance(row, list)

    def test_frame(self):
        spreadsheet = self.client.get_spreadsheet('abc123')
        sheets = spreadsheet.sheets()
        values = sheets[0].dataframe()
        self.assertIsInstance(values, pandas.DataFrame)
