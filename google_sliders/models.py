import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import OAuth2Credentials

"""
    __MAIN_OBJECTS__

    The only two objects directly retrievable through
the API
"""

class Presentation(object):

    """Google Presentation Object"""

    def __init__(self, client):
        """Class for Presentation object

        :client: <Client> from .client

        """
        self._client = client
        self._pages = []
        self._updates = []

    def __iter__(self):
        for page in self._pages:
            yield page


class Page(object):

    """Docstring for Page. """

    def __init__(self, page):
        """TODO: to be defined1.

        :page: TODO

        """
        self._page = page


"""
    __PAGE_ELEMENTS__

    Sub-Objects within the api, these elements cannot
be retrieved via http and must be derived from a page
or presentation.
"""


class PageElement(object):

    """Base Class for Slides Elements"""

    def __init__(self):
        """TODO: to be defined1. """

