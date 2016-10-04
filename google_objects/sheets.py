"""

Google Sheets Models
    Mon Sep 19 21:10:28 2016

"""
import re
import logging
from decimal import Decimal, InvalidOperation
from . import GoogleObject
from .utils import keys_to_snake

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO:
    # i/ ensure all cell data reflects table row insertion and deletion
    # ii/ page title and descriptor need to be found and initialized


class Spreadsheet(GoogleObject):

    """Represents a Google API Spreadsheet object"""

    def __init__(self, client, **kwargs):
        """Creates a new Spreadsheet Object"""

        self._client = client
        self._updates = []

        self.properties = kwargs.get('properties', {})

        # initalize the other properties
        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def from_existing(cls, client, data):
        """initiates using existing Spreadsheet resource"""

        new_data = keys_to_snake(data)
        return cls(client, **new_data)

    def __iter__(self):
        for sheet in self.sheets:
            yield sheet

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self._updates:
            self._client.push_updates(self._id, self._updates)
            # TODO: add success handlers
            del self._updates[:]

    @property
    def id(self):
        return self.__id

    @property
    def properties(self):
        return self.__properties

    @properties.setter
    def properties(self, value):
        if 'title' in value:
            self.title = value['title']

    @property
    def title(self):
        return self.__properties.get('title')

    @title.setter
    def title(self, value):
        self.__properties['title'] = value

    @property
    def sheets(self):
        return [Sheet.from_existing(self, sheet) for sheet in self.__sheets]

    @property
    def named_ranges(self):
        return self.__named_ranges

    def get_data(self, sheet_range):
        """Takes a sheet range and initializes a block object
        with the raw data and the spreadsheet for update
        functionality.
        """
        return self._client.get_values(self._id, sheet_range)


class Sheet(GoogleObject):
    """Represents a Google API Sheet object,
    there is little functionality associated with
    this object, it will be mostly used as reference for
    initializing blocks.
    """

    def __init__(self, spreadsheet=None, **kwargs):
        """Creates a new Sheet Object"""
        self._spreadsheet = spreadsheet

        self.properties = kwargs.get('properties', {})

        # initalize the other properties
        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def from_existing(cls, spreadsheet, data):
        """initiates using existing Sheet resource"""

        new_data = keys_to_snake(data)
        return cls(spreadsheet, **new_data)

    @property
    def properties(self):
        return self.__properties

    @properties.setter
    def properties(self, value):
        if 'sheet_id' in value:
            self.__properties['sheet_id'] = value['sheet_id']

        if 'title' in value:
            self.__properties['title'] = value['title']

    @property
    def id(self):
        return self.__properties.get('sheet_id')

    @property
    def title(self):
        return self.__properties.get('title')

    @title.setter
    def title(self, value):
        self.__properties['title'] = value

    def get_values(self, start=None, end=None):
        """Returns <Block> consisting of all sheet data"""
        return self._spreadsheet.get_data(self._title)


class Block(GoogleObject):
    """Recieves a dictionary corresponding to a
    ValueRange in Google Sheets and provides methods related
    to modification and formatting.
    """

    def __init__(self, client=None, spreadsheet=None, **kwargs):
        self._client = client
        self._spreadsheet = spreadsheet

        # initalize the other properties
        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def from_existing(cls, client, spreadsheet, data):
        """initiates using existing ValueRange resource"""

        new_data = keys_to_snake(data)
        return cls(client, spreadsheet, **new_data)

    def __iter__(self):
        for row in self.__values:
            yield [self.Cell(self, val) for val in row]

    def map(self, func):
        """Returns <Decimal> of block sum"""
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
            self.value = value

        @property
        def is_numerical(self):
            """Determines if value is a number, removes
            '$', ',', '.' in case of financial formatting.
            """
            try:
                Decimal(self.value)
                return True
            except InvalidOperation:
                return False

        def make_numerical(self):
            self.value = re.sub(r'[^\d.]', '', self.value)

        def match(self, regex):
            """Returns True or False if regular expression
            matches the text inside.
            """
            if self.value and re.match(regex, self.value):
                return True
            return False
