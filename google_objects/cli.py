#!/usr/bin/env python

import os
import sys
import logging

import fire

from google_objects.sheets import SheetsClient

log = logging.getLogger(__name__)


class SheetsCLI(object):

    """Command line tool for fetching tabular data
    and redirecting it to STDOUT."""

    def __init__(self, spreadsheet, key=None, service_account=False):
        """Authenticate the Google API Client and loads the Specified Spreadsheet"""

        try:
            if service_account:
                self.client = SheetsClient.from_service_account()
            else:
                self.client = SheetsClient.from_api_key(key)

            self.spreadsheet = self.client.get_spreadsheet(spreadsheet)

        except ValueError as exception:
            sys.stderr.write(str(exception))
            sys.exit(1)

    def get(self, sheet='Sheet1'):
        """Return a Google Sheet as a list of dictionaries in the 'records' attribute
        of the outputted json"""

        try:
            sheet = self.spreadsheet.get_sheet_by_name(sheet)
            dataframe = sheet.dataframe()

        except ValueError as exception:
            sys.stderr.write(str(exception))
            sys.exit(2)

        sys.stdout.write(dataframe.to_json(orient='records'))


def main():
    fire.Fire(SheetsCLI)
