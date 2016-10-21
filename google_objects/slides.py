# -*- coding: utf-8 -*-

"""

Google Slides API
    Tue 13 Sep 22:16:41 2016

"""

import re
import logging

from . import GoogleAPI, GoogleObject
from .utils import keys_to_snake, set_private_attrs

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO:
    # i/ ensure all cell data reflects table row insertion and deletion
    # ii/ page title and descriptor need to be found and initialized
    # iii/ change .from_existing to .from_raw
    # iv/ add Text nested class for Shape


class SlidesAPI(GoogleAPI):

    """Google Slides Wrapper Object

    This object wraps the Google API Slides resource
    to provide a cleaner, conciser interface when dealing
    with Google Slides objects.

    Raises exceptions, of which API object related exceptions
    are handled by its <Presentation> object.
    """

    def __init__(self, credentials, api_key):
        super(self.__class__, self).__init__(credentials)
        base_url = ('https://slides.googleapis.com/$discovery/rest?'
                        'version=v1beta1&key=' + api_key)

        self._resource = self.build('slides', 'v1beta1', discovery_url=base_url)


    def get_presentation(self, id):
        """Returns a Presentation Object

        :id: Presentation ID
        :returns: <Presentation> Model

        """
        data = self._resource.presentations().get(
            presentationId=id
        ).execute()

        return Presentation.from_existing(data, self)


    def get_page(self, presentation_id, page_id):
        """Returns a Page Object

        :id: Page ID
        :returns: <Page> Model

        """
        data = self._resource.presentations().pages().get(
            presentationId = presentation_id,
            pageObjectId = page_id
        ).execute()

        return Page.from_existing(data)

    def push_updates(self, presentation_id, updates):
        """Push Update Requests to Presentation API,
        throw errors if necessary.
        """
        presentation = self._resource.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': updates}
        ).execute()



"""
    Slides Objects:
        i/ Presentation
        ii/ Page
        iii/ Shape (Page Element)
        iv/ Table (Page Element)
"""


class Presentation(GoogleObject):

    """Google Presentation Object,
    holds batch update request lists and
    passes it to its <Client> for execution.

    """
    def __init__(self, client=None, **kwargs):
        """Class for Presentation object

        :client: <Client> from .client

        """
        self.client = client
        self.__updates = []

        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def from_existing(cls, data, client=None):
        """initiates using existing Spreadsheet resource"""

        new_data = keys_to_snake(data)
        return cls(client, **new_data)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.update()

    def __iter__(self):
        for page in self.slides:
            yield page

    def update(self):
        if self.__updates:
            self.client.push_updates(self.id, self.__updates)
            # TODO: add success handlers
            del self.__updates[:]

        return self

    def add_update(self, update):
        """Adds update of type <Dict>
        to updates list

        :update: <Dict> of update request
        :returns: <Bool> of if request was added

        """
        if type(update) is dict:
            self.__updates.append(update)
            return True
        else:
            return False

    @property
    def slides(self):
        return [Page(self, slide) for slide in self._slides]

    @property
    def masters(self):
        return [Page(self, slide) for slide in self._masters]

    @property
    def layouts(self):
        return [Page(self, slide) for slide in self._layouts]

    def get_matches(self, regex):
        """Search all Presentation text-based
        elements for matches with regex, returning
        the list of unique matches.

        :regex: a raw regex <String>
        :returns: <Set> of matches

        """
        tags = set()

        for page in self.pages:
            for element in page:
                logger.debug('Checking Element...')
                logger.debug('Type:' + str(type(element)))

                # check shape
                if type(element) is Shape:
                    if element.match(regex):
                        logger.debug('Shape MATCH')
                        tags.add(element.text)

                # check all table cells
                if type(element) is Table:
                    for row in element:
                        for cell in row:
                            if cell.match(regex):
                                logger.debug('Cell MATCH')
                                tags.add(cell.text)
        return list(tags)

    def replace_text(self, find, replace, case_sensitive=False):
        """Add update request for presentation-wide
        replacement with arg:find to arg:replace
        """
        self.add_update(
            SlidesUpdate.replace_all_text(str(find), str(replace), case_sensitive)
        )


class Page(GoogleObject):

    """Corresponds with a Page object in the Slides
    API, requires a <Presentation> object to push
    updates back up.

    args/
        :presentation // <Presentation> instance
        :kwargs // <Dict> representing API Page Resource
    """

    def __init__(self, presentation=None, **kwargs):
        self.presentation = presentation

        super(self.__class__, self).__init__(**kwargs)

    @classmethod
    def from_existing(cls, data, presentation=None):
        """initiates using existing Spreadsheet resource"""

        new_data = keys_to_snake(data)
        return cls(presentation, **new_data)

    @property
    def read_only(self):
        if not self.presentation:
            return True
        return False

    def __iter__(self):
        for element in self.elements:
            yield element

    @property
    def elements(self):
        """Generates Page elements recursively"""

        elem_list = []

        for element in self._page_elements:
            if 'elementGroup' in element:
                for child in element.get('children'):
                    elem_list.append(self.__load_element(child))

            elem_list.append(self.__load_element(element))

        return elem_list

    def __load_element(self, element):
        """Returns element object from
        slide element dict.

        :element: <Dict> repr. Page Resource Element
        :returns: <PageElement Super>

        """
        if 'shape' in element:
            return Shape(self, **element)
        elif 'table' in element:
            return Table(self, **element)
        elif 'image' in element:
            pass
        elif 'video' in element:
            pass
        elif 'wordArt' in element:
            pass
        elif 'sheetsChart' in element:
            pass

    def add_update(self, update):
        """Adds update of type <Dict>
        to updates list
        """
        return self.presentation.add_update(update)


class PageElement(GoogleObject):

    """Initialized PageElement object and
    sets metadata properties and shared object
    operations.
    """

    # TODO:
    #     i/ title and description not initializing

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(page, **kwargs)

    def update(self, update):
        return self._page.add_update(update)

    def delete(self):
        """Adds deleteObject request to
        presentation updates list.
        """
        self._page.add_update(
            SlidesUpdate.delete_object(self._id)
        )

    @property
    def id(self):
        return self._object_id

    @property
    def size(self):
        return self._size

    @property
    def transform(self):
        return self._transform


class Shape(PageElement):

    """Docstring for Shape. """

    def __init__(self, presentation=None, page=None, **kwargs):
        self.presentation = presentation
        self.page = page

        shape = kwargs.pop('shape')

        # set private attrs not done by base class
        set_private_attrs(self, shape)

        super(self.__class__, self).__init__(page, **kwargs)

        # set metadata
        self._type = shape.get('shapeType')

        # set text values
        if shape.get('text'):
            self._text = shape.get('text').get('rawText')
            self._rendered = shape.get('text').get('renderedText')
        else:
            self._text = None
            self._rendered = None

    def match(self, regex):
        """Returns True or False if regular expression
        matches the text inside.
        """
        if self.text and re.match(regex, self.text):
            return True
        else:
            return False

    @property
    def raw_text(self):
        if self._text and 'raw_text' in self._text:
            return self._text['raw_text']

    @property
    def rendered_text(self):
        if self._text and 'rendered_text' in self._text:
            return self._text['rendered_text']

    @text.setter
    def text(self, value):
        if not self._text:
            # TODO: apply deleteText
            self.update(
                SlidesUpdate.delete_text()
            )
        # TODO: apply insertText
        self.update(
            SlidesUpdate.insert_text()
        )
        self._text = value

    @text.deleter
    def text(self):
        self.update(
            SlidesUpdate.delete_text()
        )

    @property
    def type(self):
        return self._shape_type


class Table(PageElement):

    """Represents a Google Slides Table Resource"""

    # TODO:
    #     i/ add dynamic row functionality
    #     that works in tandem with corresponding cells

    def __init__(self, presentation, page, **kwargs):
        table = kwargs.pop('table')
        super(self.__class__, self).__init__(page, **kwargs)

        # initialize metadata
        self.rows = []
        self.num_rows, self.num_columns = table.get('rows'), table.get('columns')

        # initialize rows and columsn
        for row in table.get('table_rows'):
            cells = [self.Cell(self, cell) for cell in row.get('table_cells')]
            self.rows.append(cells)

    def __iter__(self):
        for row in self._rows:
            for cell in self._rows:
                yield cell

    def rows(self):
        # yield rows
        pass

    def cells(self):
        # yield cells
        pass

    class Cell(object):
        """Table Cell, only used by table"""

        def __init__(self, table, cell):
            self._table = table

            # initialize metadata
            self._row = cell.get('location').get('rowIndex')
            self._column = cell.get('location').get('columnIndex')
            self._row_span = cell.get('rowSpan')
            self._column_span = cell.get('rowColumn')
            self._text = None
            self._rendered = None

            # initialize values
            if 'text' in cell:
                self._text = cell.get('text').get('rawText')
                self._rendered = cell.get('text').get('renderedText')

        def match(self, regex):
            """Returns True or False if regular expression
            matches the text inside.
            """
            if self.text and re.match(regex, self.text):
                return True
            else:
                return False

        @property
        def text(self):
            return self._text

        @text.setter
        def text(self, value):
            if not self._text:
                # TODO: apply deleteText
                self._table.update(
                    SlidesUpdate.delete_text()
                )

            # TODO: apply insertText
            self._table.update(
                SlidesUpdate.insert_text()

            )
            self._text = value

        @text.deleter
        def text(self):
            self._table.update(
                SlidesUpdate.delete_text()
            )
            self._text = None



"""Helper Classes"""

class DELETE_MODES:
    DELETE_ALL = 'DELETE_ALL'


class SlidesUpdate(object):

    """creates google-api-wrapper ready batchUpdate
    request dictionaries
    """

    @staticmethod
    def delete_object(obj_id):
        return {
            'deleteObject': {
                'objectId': obj_id
            }
        }

    @staticmethod
    def replace_all_text(find, replace, case_sensitive=False):
        return {
            'replaceAllText': {
                'findText': find,
                'replaceText': replace,
                'matchCase': case_sensitive
            }
        }

    @staticmethod
    def insert_text(obj_id, text, row=None, column=None, insertion_index=0):
        return {
            'insertText': {
                'objectId': obj_id,
                'text': text,
                'cellLocation': {
                    'rowIndex': row,
                    'columnIndex': column
                },
                'insertionIndex': insertion_index

            }
        }
        pass

    @staticmethod
    def delete_text(obj_id, row=None, column=None, mode='DELETE_ALL'):
        return {
            'deleteText': {
                'objectId': obj_id,
                'cellLocation': {
                    'rowIndex': row,
                    'columnIndex': column
                },
                'deleteMode': mode
            }
        }
