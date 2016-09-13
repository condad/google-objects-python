import re
import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials


SCOPES = 'https://www.googleapis.com/auth/drive'
USER_EMAIL = 'team@xyzfoundation.com'
API_KEY = 'AIzaSyBe7-2oJUa_Gyl4SdDdPfLRymCKCdeb0zU'


class Client(object):
    """Google Slides Wrapper Object

    This object wraps the Google API Slides resource
    to provide a cleaner, conciser interface when dealing
    with Google Slides objects.
    """

    def __init__(self, credentials, api_key):
        self._auth = credentials
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://slides.googleapis.com/$discovery/rest?'
                        'version=v1beta1&key=' + api_key)
        self._resource = discovery.build('slides', 'v1beta1', http=http,
                                discoveryServiceUrl=discoveryUrl)

    def open(self, id):
        """Return Presentation Object"""
        pass

    def get_presentation(self, id):
        """returns an initialized presentation
        object

        :id: Slides Presentation ID
        :returns: <Presentation> object

        """
        pass

    def get_page(self, presentation, page):
        """execute page api call and initializes a page
        with a presentation object

        :presentation: TODO
        :page: TODO
        :returns: TODO

        """
        pass

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

    def batch_update(self, updates):
        self._resource.presentations().batchUpdate(
            presentationId = self._slide_id,
            body={
                'requests': updates
            }
        ).execute()
        # empty list afterwards
        del self._updates[:]

    def create(self, title):
        """TODO: Docstring for create.

        :title: TODO
        :returns: new presentation object

        """
        pass

    def _append_update(self, update):
        self._updates.append(update)
