# -*- coding: utf-8 -*-

"""

Google Slides API
    Tue 13 Sep 22:16:41 2016

"""

import logging
import functools

from google_objects.core import GoogleClient
from google_objects.core import GoogleObject

log = logging.getLogger(__name__)


class SlidesClient(GoogleClient):

    """Google Slides Wrapper Object

    This object wraps the Google API Slides resource
    to provide a cleaner, conciser interface when dealing
    with Google Slides objects.

    Raises exceptions, of which API object related exceptions
    are handled by its <Presentation> object.
    """

    service = 'slides'
    version = 'v1'
    scope = {'slides'}

    def get_presentation(self, presentation_id):
        """Returns a Presentation Object

        :id: Presentation ID
        :returns: <Presentation> Model

        """
        data = self.resource.presentations().get(
            presentationId=presentation_id
        ).execute()

        return Presentation.from_existing(data, self)

    def get_page(self, presentation_id, page_id):
        """Returns a Page Object

        :id: Page ID
        :returns: <Page> Model

        """
        data = self.resource.presentations().pages().get(
            presentationId=presentation_id,
            pageObjectId=page_id
        ).execute()

        return Page.from_existing(data)

    def push_updates(self, presentation_id, updates):
        """Push Update Requests to Presentation API,
        throw errors if necessary.
        """
        self.resource.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': updates}
        ).execute()


class Presentation(GoogleObject):

    """Google Presentation Object,
    holds batch update request lists and
    passes it to its <Client> for execution.
    """

    _properties = {
        'presentationId',
        'layouts',
        'slides',
        'masters',
    }

    def __init__(self, client=None, **kwargs):
        """Class for Presentation object

        :client: <Client> from .client

        """
        self.client = client
        self.__updates = []

        super().__init__(**kwargs)

    @classmethod
    def from_existing(cls, data, *args):
        return cls(*args, **data)

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_val, traceback):
        self.update()
        return True

    def __iter__(self):
        for page in self.slides():
            yield page

    @property
    def id(self):
        return self.data['presentationId']

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

    def slides(self):
        return [Page(self, **slide) for slide in self.data['slides']]

    def masters(self):
        return [Page(self, **slide) for slide in self.data['masters']]

    def layouts(self):
        return [Page(self, **slide) for slide in self.data['layouts']]

    def elements(self):
        for page in self.slides():
            for element in page:
                yield element

    def replace_text(self, find, replace, case_sensitive=False):
        """Add update request for presentation-wide
        replacement with arg:find to arg:replace
        """
        ud = REPLACE_ALL_TEXT(str(find), str(replace), case_sensitive)
        self.add_update(ud)

    def get_element_by_id(self, element_id):
        """Retrieves an element within this presentation identified
        by the argument given. Returns None if no such element is found.

        :element_id: string representing element id
        :returns: <PageElement> object or None

        """
        for page in self.slides():
            log.debug('Page: {}'.format(type(page)))
            if element_id in page:
                return page[element_id]


class Page(GoogleObject):

    """Corresponds with a Page object in the Slides
    API, requires a <Presentation> object to push
    updates back up.

    args/
        :presentation // <Presentation> instance
        :kwargs // <Dict> representing API Page Resource
    """

    _properties = {
        'pageElements'
    }

    def __init__(self, presentation=None, **kwargs):
        self.presentation = presentation
        super().__init__(**kwargs)

    @property
    def id(self):
        return self.data['objectId']

    @property
    def read_only(self):
        if not self.presentation:
            return True
        return False

    def __load_element(self, element):
        """Returns element object from
        slide element dict.

        :element: <Dict> repr. Page Resource Element
        :returns: <PageElement Super>

        """
        if 'shape' in element:
            log.debug('Shape %s loaded.', element['objectId'])
            return Shape(self.presentation, self, **element)
        elif 'table' in element:
            log.debug('Table %s loaded.', element['objectId'])
            return Table(self.presentation, self, **element)
        elif 'element_group' in element:
            log.debug('Element Group %s loaded.', element['objectId'])
            return [self.__load_element(each) for each in element['children']]

        # TODO: Implement the following constructors
        elif 'image' in element:
            log.debug('Image %s loaded.', element['objectId'])
            return PageElement(self.presentation, self, **element)
        elif 'video' in element:
            log.debug('Video %s loaded.', element['objectId'])
            return PageElement(self.presentation, self, **element)
        elif 'word_art' in element:
            log.debug('Word Art %s loaded.', element['objectId'])
            return PageElement(self.presentation, self, **element)
        elif 'sheets_chart' in element:
            log.debug('Sheets Chart %s loaded.', element['objectId'])
            return PageElement(self.presentation, self, **element)

    def yield_elements(self, __sub_list=[]):
        """Generates PageElement objects according to type.

        *NEVER pass an argument to this function, the parameter
        is only to add recursive list flattening with respect to
        nested element groups.
        """
        for element in __sub_list or self.data['pageElements']:
            if isinstance(element, list):
                self.yield_elements(element)

            yield self.__load_element(element)

    def elements(self):
        """Return a list of PageElement instances."""
        return [element for element in self.yield_elements()]

    def __iter__(self):
        return self.yield_elements()

    def __contains__(self, element_id):
        """Checks if this page contains elements referred to
        by argument.

        :element_id: Unique Google PageElement ID string.
        :returns: True or False

        """
        element_id_set = set()
        for each in self.yield_elements():
            if each:
                element_id_set.add(each.id)

        return element_id in element_id_set

    def __getitem__(self, element_id):
        """Returns element within presentation identified
        by the given argument, raises TypeError
        if such element isn't present.
        """
        for element in self.yield_elements():
            if element_id == element.id:
                return element

        raise TypeError


class PageElement(GoogleObject):

    """Initialized PageElement object and
    sets metadata properties and shared object
    operations.
    """

    _types = {'shape', 'table', 'image', 'video', 'word_art', 'sheets_chart'}

    # TODO:
    #     i/ title and description not initializing

    def __init__(self, presentation=None, page=None, **kwargs):
        self.presentation = presentation
        self.page = page

        super().__init__(**kwargs)

    @property
    def id(self):
        return self.data['objectId']

    @property
    def size(self):
        return self.data['size']

    @property
    def transform(self):
        return self.data['transform']

    def update(self, update):
        return self.presentation.add_update(update)

    def delete(self):
        """Adds deleteObject request to
        presentation updates list.
        """
        ud = DELETE_OBJECT(self.data.id)
        self.presentation.add_update(ud)


class Shape(PageElement):

    """Docstring for Shape."""

    def __init__(self, presentation=None, page=None, **kwargs):
        super().__init__(presentation, page, **kwargs)

        shape = kwargs.pop('shape')
        self.data.update(shape)

    @property
    def text(self):
        if self.data.get('text'):
            return TextContent(
                self.presentation,
                self.page,
                self,
                **self.data['text']
            )

    @property
    def type(self):
        return self.data['shapeType']


class Table(PageElement):

    """Represents a Google Slides Table Resource"""

    # TODO:
    #     i/ add dynamic row functionality
    #     that works in tandem with corresponding cells

    def __init__(self, presentation=None, page=None, **kwargs):
        super().__init__(presentation, page, **kwargs)

        table = kwargs.pop('table')
        self.data.update(table)

    def __iter__(self):
        return self.cells()

    def rows(self):
        for row in self.data['tableRows']:
            yield [self.Cell(self, cell) for cell in row.get('tableCells')]

    def cells(self):
        for row in self.data['tableRows']:
            for cell in row.get('tableCells'):
                yield self.Cell(self, **cell)

    def get_cell(self, row, column):
        """Fetches cell data and returns as object."""

        cell_data = self.data['tableRows'][row]['tableCells'][column]
        return self.Cell(self, **cell_data)

    class Cell(GoogleObject):
        """Table Cell, only used by table"""

        def __init__(self, table, **kwargs):
            self.table = table
            super().__init__(**kwargs)

        @property
        def text(self):
            if hasattr(self, '_text'):
                return TextContent(
                    self.table.presentation,
                    self.table.page,
                    self.table,
                    **self.data.text
                )

        @property
        def location(self):
            return self.data['location']

        @property
        def row_index(self):
            return self.location['row_index']

        @property
        def column_index(self):
            return self.location['column_index']

        @property
        def position(self):
            return self.row_index, self.column_index


class TextContent(GoogleObject):

    """Docstring for TextElement. """

    _properties = {'textElements, lists'}

    def __init__(self, presentation=None, page=None, element=None, **kwargs):
        self.presentation = presentation
        self.page = page
        self.element = element

        super().__init__(**kwargs)

    def yield_elements(self):
        for text_element in self.data['textElements']:
            yield TextElement(self, self.element, **text_element)

    def elements(self):
        return [elem for elem in self.yield_elements()]

    def __iter__(self):
        self.yield_elements()


class TextElement(GoogleObject):

    _properties = {
        'startIndex',
        'endIndex',
        'paragraphMarker',
        'textRun',
        'autoText'
    }

    def __init__(self, text_content, page_element, **kwargs):
        self.text_content = text_content
        self.page_element = page_element

        # set update partials
        self.delete_text = functools.partial(
            DELETE_TEXT,
            row=getattr(self.page_element, 'startIndex', None),
            col=getattr(self.page_element, 'endIndex', None),
            start=self.startIndex,
            end=self.end_index
        )
        self.insert_text = functools.partial(
            INSERT_TEXT,
            obj_id=self.id,
            start=self.start_index
        )

        super().__init__(**kwargs)

    @property
    def start_index(self):
        return self.data['startIndex']

    @property
    def end_index(self):
        return self.data['endIndex']

    @property
    def segment(self):
        return self.start_index, self.end_index

    @property
    def text_run(self):
        return self.data.get('text_run')

    @property
    def text(self):
        if self.text_run:
            return self.text_run['content']

    @text.setter
    def text(self, value):
        if not self.data.text:
            ud = DELETE_TEXT(
                self.page_element.id,
                row=getattr(self.page_element, 'startIndex', None),
                col=getattr(self.page_element, 'endIndex', None),
                start=self.start_index,
                end=self.end_index
            )
            self.page_element.update(ud)

        update_request = INSERT_TEXT(
            value, self.id, start=self.start_index
        )
        self.page_element.update(update_request)

        self.text_run['content'] = value

    @text.deleter
    def text(self):
        obj_id = self.page_element.id
        update_request = DELETE_TEXT(
            obj_id, start=self.start_index, end=self.end_index
        )
        self.page_element.update(update_request)

    def __str__(self):
        return self.text


def DELETE_OBJECT(obj_id):
    return {
        'deleteObject': {
            'objectId': obj_id
        }
    }


def REPLACE_ALL_TEXT(find, replace, case_sensitive=False):
    return {
        'replaceAllText': {
            'replaceText': replace,
            'containsText': {
                'text': find,
                'matchCase': case_sensitive
            }
        }
    }


def INSERT_TEXT(text, obj_id=None, row=None, column=None, start=0):
    return {
        'insertText': {
            'objectId': obj_id,
            'text': text,
            'cellLocation': {
                'rowIndex': row,
                'columnIndex': column
            },
            'insertionIndex': start

        }
    }


def DELETE_TEXT(obj_id, row=None,
                col=None, start=None, end=None, kind='FIXED_RANGE'):
    return {
        'deleteText': {
            'objectId': obj_id,
            'cellLocation': {
                'rowIndex': row,
                'columnIndex': col
            },
            'text_range': {
                'startIndex': start,
                'endIndex': end

            },
        }
    }
