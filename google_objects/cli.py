#!/usr/bin/env python

import os
import sys
import json
import logging

import fire
import pandas as pd

from google_objects.sheets import SheetsClient

log = logging.getLogger(__name__)


class SheetsCLI(object):

    """Command line tool for fetching tabular data
    and redirecting it to STDOUT."""

    def __init__(self, key=None, service_account=False, user=None):
        """Authenticate the Google API Client and loads the Specified Spreadsheet"""

        try:
            if service_account:
                self.client = SheetsClient.from_service_account(user=user)
            else:
                self.client = SheetsClient.from_api_key(key)

        except ValueError as exception:
            sys.stderr.write(str(exception))
            sys.exit(1)

    def get_spreadsheet(self, spreadsheet_id):
        """Return a Google Sheet as a list of dictionaries in the 'records' attribute
        of the outputted json"""

        try:
            spreadsheet = self.client.get_spreadsheet(spreadsheet_id)
            output = {
                'title': spreadsheet.title,
                'id': spreadsheet.id,
                'sheets': [{'title': sheet.title,
                            'records': sheet.dataframe().to_dict(
                                orient='records')}
                           for sheet in spreadsheet.sheets()]
                }

        except ValueError as exception:
            sys.stderr.write(str(exception))
            sys.exit(2)

        #  sys.stdout.write(dataframe.to_json(orient='records'))
        sys.stdout.write(json.dumps(output))

    def create_spreadsheet(self, file_path=None):
        """Create a new Google Spreadsheet. 

        :file_name: JSON File name
        :returns: URL of newly created Google Sheet.

        """
        if file_path:
            with open(file_path, 'r') as f:
                json_data = f.read()
        else:
            json_data = sys.stdin.read()

        input_data = json.loads(json_data)
        if 'records' in input_data:
            input_data = input_data['records']

        df = pd.DataFrame(input_data)
        try:
            spreadsheet = self.client.create_spreadsheet_from_dataframe(df)
            sys.stdout.write(spreadsheet.url)
        except Exception as e:
            sys.stdout.write(e)


def main():
    fire.Fire(SheetsCLI)
