"""

Google Slides API HTTP Resource
    Tue 13 Sep 22:17:15 2016

"""
import os
import re
import logging
import httplib2

from .slides import Presentation, Page
from .sheets import Spreadsheet
from apiclient import discovery
from apiclient.errors import HttpError

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO:
#     i/ type match credentials
#     ii/ start exception handling


def _find_credentials(name='xyz_creds.json'):
    """finds credentials within project

    :name: name of credential file
    :returns: full path to credentials

    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'lab/google-objects/.credentials')
    credential_path = os.path.join(credential_dir, name)
    return credential_path


class GoogleAPI(object):
    """Google API Base object that saves credentials
    and build Resource objects. Responsible for permissions
    as well.

    """
    def __init__(self, credentials):
        self._credentials = credentials

    def build(self, service, version, discovery_url):
        http = self._credentials.authorize(httplib2.Http())
        return discovery.build(service, version, http=http, discoveryServiceUrl=discovery_url)

    def get_permissions(self, api):
        pass


class SlidesAPI(GoogleAPI):
    """Google Slides Wrapper Object

    This object wraps the Google API Slides resource
    to provide a cleaner, conciser interface when dealing
    with Google Slides objects.

    Raises exceptions, of which API object related exceptions
    are handled by its <Presentation> object.
    """

    def __init__(self, credentials, api_key, **kwargs):
        super(self.__class__, self).__init__(credentials)
        base_url = ('https://slides.googleapis.com/$discovery/rest?'
                        'version=v1beta1&key=' + api_key)

        self._resource = self.build('slides', 'v1beta1', discovery_url=base_url)


    def presentation(self, id):
        """Returns a Presentation Object

        :id: Presentation ID
        :returns: <Presentation> Model

        """
        presentation_raw = self._resource.presentations().get(
            presentationId = id
        ).execute()

        return Presentation(self, presentation_raw)


    def page(self, presentation_id, page_id):
        """Returns a Page Object

        :id: Page ID
        :returns: <Page> Model

        """
        page_raw = self._resource.presentations().pages().get(
            presentationId = presentation_id,
            pageObjectId = page_id
        ).execute()

        return Page(page_raw)


    @classmethod
    def get_presentation(cls, credentials, id, api_key=None):
        """Retrieves an initialized <Presentation>
        object, passes itself.

        :id: Slides Presentation ID
        :returns: <Presentation>

        """
        client = cls(credentials, api_key)
        return client.presentation(id)


    @classmethod
    def get_page(cls, credentials, presentation_id, page_id, api_key=None):
        """Retrieves an existing <Page>
        and initializes it with and existing
        <Presentation> object. Page is READ ONLY.

        :presentation_id: Slides Presentation ID
        :page: Slides Page ID
        :returns: <Page>

        """
        client = cls(credentials, api_key)
        return client.page(presentation_id, page_id)


    def push_updates(self, presentation_id, updates):
        self._resource.presentations().batchUpdate(
            presentationId = presentation_id,
            body={
                'requests': updates
            }
        ).execute()


class SheetsAPI(GoogleAPI):

    """Creates a Google Sheets Resource"""

    def __init__(self, credentials, **kwargs):
        super(self.__class__, self).__init__(credentials, **kwargs)
        base_url = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')

        self._resource = self.build('sheets', 'v4', discovery_url=base_url)


    def spreadsheet(self, id):
        """Returns a Spreadsheet Object

        :id: Spreadsheet ID
        :returns: <Spreadsheet> Model

        """
        spreadsheet_raw = self._resource.spreadsheets().get(
            spreadsheetId = id
        ).execute()

        return Spreadsheet(self, spreadsheet_raw)

    def range(self, sheet_range):

        sheet_range


    @classmethod
    def get_spreadsheet(cls, credentials, id):
        """Retrieves an initialized <Spreadsheet>
        object, passes itself.

        :id: Sheets ID
        :returns: <Spreadsheet>

        """
        client = cls(credentials)
        return client.presentation(id)


    def push_updates(self, spreadsheet_id, updates):
        self._resource.spreadsheets().batchUpdate(
            presentationId = spreadsheet_id,
            body={
                'requests': updates
            }
        ).execute()
