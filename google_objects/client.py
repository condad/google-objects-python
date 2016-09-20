"""

Google Slides API HTTP Resource
    Tue 13 Sep 22:17:15 2016

"""
import os
import re
import logging
import httplib2

from .slides import Presentation, Page
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


class Client(object):
    """Google Slides Wrapper Object

    This object wraps the Google API Slides resource
    to provide a cleaner, conciser interface when dealing
    with Google Slides objects.

    Raises exceptions, of which API object related exceptions
    are handled by its <Presentation> object.
    """

    def __init__(self, credentials, base_url):
        self._auth = credentials
        self._resource = None
        base_url = ('https://slides.googleapis.com/$discovery/rest?'
                        'version=v1beta1&key=' + api_key)
        self._resource = discovery.build('slides', 'v1beta1', http=http,
                                discoveryServiceUrl=base_url)


    @classmethod
    def get_presentation(cls, credentials, id, api_key=None):
        """Retrieves an initialized <Presentation>
        object, passes itself.

        :id: Slides Presentation ID
        :returns: <Presentation>

        """
        base_url = ('https://slides.googleapis.com/$discovery/rest?'
                        'version=v1beta1&key=' + api_key)

        client = cls(credentials, base_url)
        http = client.credentials.authorize(httplib2.Http())
        client._resource = discovery.build('slides', 'v1beta1', http=http,
                                discoveryServiceUrl=base_url)

        presentation_raw = self._resource.presentations().get(
            presentationId = id
        ).execute()

        return Presentation(self, presentation_raw)


    @classmethod
    def get_page(self, credentials, presentation_id, page_id, api_key=None):
        """Retrieves an existing <Page>
        and initializes it with and existing
        <Presentation> object. Page is READ ONLY.

        :presentation_id: Slides Presentation ID
        :page: Slides Page ID
        :returns: <Page>

        """
        base_url = ('https://slides.googleapis.com/$discovery/rest?'
                        'version=v1beta1&key=' + api_key)

        client = cls(credentials, base_url)
        http = client.credentials.authorize(httplib2.Http())
        client._resource = discovery.build('slides', 'v1beta1', http=http,
                                discoveryServiceUrl=base_url)

        page_raw = self._resource.presentations().pages().get(
            presentationId = presentation_id,
            pageObjectId = page_id
        ).execute()

        return Page(page_raw)


    def push_updates(self, presentation_id, updates):
        print updates
        self._resource.presentations().batchUpdate(
            presentationId = presentation_id,
            body={
                'requests': updates
            }
        ).execute()
