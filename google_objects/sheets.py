"""

Google Sheets Models
    Mon Sep 19 21:10:28 2016

"""
import re
import logging
from decimal import Decimal, InvalidOperation
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
        self._id = spreadsheet.get('spreadsheetId')


        if 'properties' in spreadsheet:
            self._title = spreadsheet['properties'].get('title')
            self._locale = spreadsheet['properties'].get('locale')
        else:
            self._title = None
            self._locale = None

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
        """Returns <List> of Named
        Ranges of Spreadsheet
        """
        return self._named_ranges


    def get_data(self, sheet_range):
        """Takes a sheet range and initializes a block object
        with the raw data and the spreadsheet for update
        functionality.
        """
        return self._client.values_get(self._id, sheet_range)


class Sheet(object):
    """Represents a Google API Sheet object,
    there is little functionality associated with
    this object, it will be mostly used as reference for
    initializing blocks.
    """

    def __init__(self, sheet, spreadsheet):
        """Creates a new Sheet Object"""
        self._spreadsheet = spreadsheet
        self._data = sheet.get('data')

        if 'properties' in sheet:
            self._id = sheet['properties'].get('id')
            self._title = sheet['properties'].get('title')
            self._locale = sheet['properties'].get('locale')
        else:
            self._id = None
            self._title = None
            self._locale = None

    def get_values(self):
        """Return <Block> consisting of all sheet data"""
        return self._spreadsheet.get_data(self._title)



class Block(object):
    """Recieves a dictionary corresponding to a
    ValueRange in Google Sheets and provides methods related
    to modification and formatting.
    """

    def __init__(self, client, values):
        self._client = client
        self._updates = []
        self._rows = []

        for row in values.get('values'):
            cells = [self.Cell(self, value) for value in row]
            self._rows.append(cells)

    def __iter__(self):
        for row in self._rows:
            yield row

    def map(self, func):
        """Returns <Decimal> of block sum"""
        total = Decimal()
        for row in self._rows:
            for cell in row:
                cell.value = func(cell)


    @property
    def is_numerical(self):
        for row in self._rows:
            for cell in row:
                if not cell.is_number:
                    return False
        return True


    class Cell(object):
        """Represents a Google Sheets Cell, each value
        is initially <unicode>
        """
        def __init__(self, block, value):
            self._block = block
            self._value = value

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, value):
            # TODO:
            #     add update request
            self._value = value

        @property
        def is_number(self):
            """Determines if value is a number, removes
            '$', ',', '.' in case of financial formatting.
            """
            try:
                Decimal(self.value)
                return True
            except InvalidOperation:
                return False

        def make_number(self):
            self.value = re.sub(r'[^\d.]', '', self.value)

        def match(self, regex):
            """Returns True or False if regular expression
            matches the text inside.
            """
            if self.value and re.match(regex, self.value):
                return True
            return False
