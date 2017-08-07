import unittest
from unittest import mock

from tests.utils import get_data
from google_objects.sheets.core import SheetsClient
from google_objects.sheets.core import Spreadsheet
from google_objects.sheets.core import Sheet
from google_objects.sheets.core import Block

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
        self.assertEqual(type(spreadsheet), Spreadsheet)

        # test spreadsheet properties
        self.assertEqual(spreadsheet.title, 'Test Google Spreadsheet')
        self.assertEqual(spreadsheet.id, 'abc123')

    def test_sheets(self):
        spreadsheet = self.client.get_spreadsheet('abc123')
        sheets = spreadsheet.sheets()

        for i, sheet in enumerate(sheets):
            self.assertEqual(type(sheet), Sheet)

        first_sheet = sheets[0]
        self.assertEqual(first_sheet.title, 'CLSFF Fluxx')

    def test_values(self):
        spreadsheet = self.client.get_spreadsheet('abc123')
        sheets = spreadsheet.sheets()
        values = sheets[0].values()
        self.assertEqual(type(values), Block)

        for val in values:
            self.assertEqual(type(val), list)
