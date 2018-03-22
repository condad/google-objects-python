#!/usr/bin/env python

import os
import logging

import fire

from google_objects.sheets import SheetsClient

log = logging.getLogger(__name__)


class SheetsCLI(object):

    """Command line tool for fetching tabular data
    and redirecting it to STDOUT."""

    def __init__(self, spreadsheet=None, key=None):
        """Authenticate the Google API Client and loads the Specified Spreadsheet"""

        if not spreadsheet:
            raise ValueError("Spreadsheet argument required.")

        if not key:
            key = os.getenv('GOOGLE_SHEETS_API_KEY')

        if key:
            self.client = SheetsClient.from_api_key(key)
        else:
            err_msg = "Valid API Key required, as argument or env variable set to GOOGLE_SHEETS_API_KEY."
            raise ValueError(err_msg)
            #  self.client = SheetsClient.from_service_account()

        self.spreadsheet = self.client.get_spreadsheet(spreadsheet)

    def get(self, sheet='Sheet1'):
        """Return a Google Sheet as a list of dictionaries in the 'records' attribute
        of the outputted json"""

        sheet = self.spreadsheet.get_sheet_by_name(sheet)
        dataframe = sheet.frame()

        print(dataframe.to_json(orient='records'))


def main():
    fire.Fire(SheetsCLI)
