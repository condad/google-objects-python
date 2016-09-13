import importlib
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

    """Google Presentation Object

    attributes/

        _client: <Client> -- http interface
        _pages: <Page List> -- list of Page objects


    """

    def __init__(self, client, presentation):
        """Class for Presentation object

        :client: <Client> from .client

        """
        self._client = client
        self._pages = []
        self._updates = []

    def __iter__(self):
        for page in self._pages:
            yield page

    def update(self):
        self._resource.presentations().batchUpdate(
            presentationId = self._slide_id,
            body={
                'requests': updates
            }
        ).execute()
        self._client.batch_update(self._updates)

        # TODO: add success handlers
        # empty list afterwards if successfull
        del self._updates[:]

    def __getattr__(self, name):
        """Handle sub-class instantiation.

        Args:
            name (str): Name of model to instantiate.

        Returns:
            Instance of named class.
        """
        try:
            # api class first
            model = getattr(importlib.import_module(
                __package__ + '.' + name.lower()), name)

            self._log.debug('loaded instance of api class %s', name)
            return model(self)
        except ImportError:
            try:
                model = getattr(importlib.import_module(
                    name.lower()), name)
                self._log.debug('loaded instance of model class %s', name)
                return model()
            except ImportError:
                self._log.debug('ImportError! Cound not load api or model class %s', name)
                return name


class Page(object):

    """Docstring for Page. """

    def __init__(self, presentation, page):
        """Class for Page object

        :page: TODO

        """
        self._page = page
        self._elements = []


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


class Table(PageElement):

    """Docstring for Table. """

    def __init__(self, table):
        """TODO: to be defined1.

        :table: dict w/ table object

        """
        PageElement.__init__(self)

        self._table = table
