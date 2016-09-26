"""

Google Sheets Models
    Mon Sep 19 21:10:28 2016

"""
import re
import logging
# from .utils import >>>

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO:
    # i/ ensure all cell data reflects table row insertion and deletion
    # ii/ page title and descriptor need to be found and initialized


"""Spreadsheet"""

class Spreadsheet(object):

    """Represents a Google API Spreadsheet object"""

    def __init__(self, client, spreadsheet):
        """Creates a new Spreadsheet Object"""

        self._client = client
        self._updates = []

        # load presentation metadata
        self._id = spreadsheet.get('spreadsheetId')
        self._title = None
        self._locale = None

        if 'properties' in spreadsheet:
            self._title = spreadsheet['properties'].get('title')
            self._locale = spreadsheet['properties'].get('locale')

        self._sheets = [Sheet(sheet, self) for sheet in spreadsheet.get('sheets')]
        self._named_ranges = spreadsheet.get('namedRanges')

    def __iter__(self):
        for sheet in self._sheets:
            yield sheet

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.update()
        return True

    def update(self):
        if self._updates:
            self._client.push_updates(self._id, self._updates)
            # TODO: add success handlers
            del self._updates[:]

    def named_ranges(self):
        """Returns List of Named
        Ranges of Spreadsheet
        """
        return self._named_ranges


class Sheet(object):

    """Represents a Google API Sheet object"""

    def __init__(self, sheet, spreadsheet):
        """Creates a new Sheet Object"""
        self._spreadsheet = spreadsheet
        self._id = None
        self._title = None
        self._locale = None
        self._data = None
        self.data = sheet

        if 'properties' in sheet:
            self._id = sheet['properties'].get('id')
            self._title = sheet['properties'].get('title')
            self._locale = sheet['properties'].get('locale')

        if 'data' in sheet:
            self._data = [Grid(grid, self) for grid in sheet.get('data')]

        if 'merges' in sheet:
            self._data = [Grid(grid, self) for grid in sheet.get('merges')]


class Grid(object):

    """Represents Grid Data In Google Sheets"""

    def __init__(self, grid, sheet):
        self._sheet = sheet

        self.data = grid
