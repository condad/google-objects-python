"""

Google Slides API HTTP Resource
    Tue 13 Sep 22:17:15 2016

"""
import re
import logging
import httplib2

from google_sliders.models import Presentation, Page
from apiclient import discovery
from apiclient.errors import HttpError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Client(object):
    """Google Slides Wrapper Object

    This object wraps the Google API Slides resource
    to provide a cleaner, conciser interface when dealing
    with Google Slides objects.

    Raises exceptions, of which API object related exceptions
    are handled by its <Presentation> object.
    """

    def __init__(self, credentials, api_key):
        self._auth = credentials
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://slides.googleapis.com/$discovery/rest?'
                        'version=v1beta1&key=' + api_key)
        self._resource = discovery.build('slides', 'v1beta1', http=http,
                                discoveryServiceUrl=discoveryUrl)


    def get_presentation(self, id):
        """Retrieves an initialized <Presentation>
        object, passes itself.

        :id: Slides Presentation ID
        :returns: <Presentation>

        """
        presentation_raw = self._resource.presentations().get(
            presentationId = id
        ).execute()

        return Presentation(self, presentation_raw)


    def get_page(self, presentation_id, page_id):
        """Retrieves an existing <Page>
        and initializes it with and existing
        <Presentation> object. Page is READ ONLY.

        :presentation_id: Slides Presentation ID
        :page: Slides Page ID
        :returns: <Page>

        """
        page_raw = self._resource.presentations().pages().get(
            presentationId = presentation_id,
            pageObjectId = page_id
        ).execute()

        print len(page_raw)

        return Page(page_raw)


    def push_updates(self, presentation_id, updates):
        print updates
        self._resource.presentations().batchUpdate(
            presentationId = presentation_id,
            body={
                'requests': updates
            }
        ).execute()


    def get_tags(self):
        """TODO: Docstring for get_tags.
        :returns: TODO

        """
        tags = set()
        presentation = self._resource.presentations().get(
            presentationId = self._slide_id
        ).execute()

        for slide in presentation['slides']:
            for element in slide['pageElements']:
                values = self._get_values(element)
                for value in values:
                    tags.add(value)

        return tags


    def _get_values(self, element):
        """Returns text value string list of
        a Slides API PageElement

        :element: <Dict> // Google Slides PageElement
        :returns: <List> // all text values in given element

        """
        values = []

        if 'table' in element:
            rows = element['table']['tableRows']
            for row in rows:
                for cell in row['tableCells']:
                    value = cell['text']['rawText']
                    tag = re.match(r'{{.*?}}', value)
                    if tag:
                        values.append(value[2:-2])
        elif 'shape' in element:
            pass
        # TODO:
        #     shape
        #     element_groups
        #     etc

        return values

    def update_cell(self, table_id, row, column, value):
        self._resource.presentations().batchUpdate(
            presentationId = self._slide_id,
            body={
                'requests': [
                    {
                        'deleteText': {
                            'objectId': table_id,
                            'cellLocation': {
                                'rowIndex': row,
                                'columnIndex': column
                            },
                            'deleteMode': 'DELETE_ALL'
                        }
                    },
                    {
                        'insertText': {
                            'objectId': table_id,
                            'cellLocation': {
                                'rowIndex': row,
                                'columnIndex': column
                            },
                            'text': value
                        }
                    },
                ]
            }
        ).execute()
