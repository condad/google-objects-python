"""

Google Slides Models
    Tue 13 Sep 22:16:41 2016

"""
import importlib


class Presentation(object):
    """Google Presentation Object,
    holds batch update request lists and
    passes it to its <Client> for execution.

    """
    def __init__(self, client, presentation):
        """Class for Presentation object

        :client: <Client> from .client

        """
        self._client = client
        self._updates = []

        # load presentation metadata

        self._id = presentation.get('presentationId')
        self._title = presentation.get('title')
        self._locale = presentation.get('local')
        self._width = presentation.get('size').get('width')
        self._length = presentation.get('size').get('length')

        # load page objects

        # i/
        self._pages = [Page(self, page) for page in presentation.get('pages')]
        self._masters = [Page(self, page) for page in presentation.get('masters')]
        self._layouts = [Page(self, page) for page in presentation.get('layouts')]

        # ii/
        # page_lsts = presentation.get('pages'), \
        #     presentations.get('masters'), \
        #     presentations.get('layouts')

        # self._slides, \
        # self._masters, \
        # self._layouts = (
        #     map(lambda page: Page(self, page), page_lst)
        #     for page_lst in page_lsts
        # )


    def __iter__(self):
        for page in self._pages:
            yield page


    def __exit__(self, exception_type, exception_value, traceback):
        try:
            self.update()
            return True
        except:
            return False


    def update(self):
        self.client.update(self._updates)

        # TODO: add success handlers
        del self._updates[:]


    def add_update(self, update):
        """Adds update of type <Dict>
        to updates list

        :update: <Dict> of update request
        :returns: <Bool> of if request was added

        """
        if type(update) is dict:
            self._updates.append(update)
            return True
        else:
            return False


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
        self._presentation = presentation

        # load metadata
        self._id = page.get('objectId')
        self._type = page.get('pageType')
        self._elements = []

        # load elements
        for element in page.get('pageElements'):
            self._elements.append(self._load_element(element))


    def _load_element(self, element):
        """Initialize element object from
        from slide element dict

        :elements: <Dict>
        :returns: NONE

        """
        if 'elementGroup' in element:
            for child in element.get('children'):
                self._load_element(child)
            return
        elif 'shape' in element:
            pass
        elif 'image' in element:
            pass
        elif 'video' in element:
            pass
        elif 'table' in element:
            obj = Table(self._presentation, self, **element)
            pass
        elif 'wordArt' in element:
            pass
        elif 'sheetsChart' in element:
            pass

        self._elements.append(obj)

    def add_update(self, update):
        """Adds update of type <Dict>
        to updates list

        :update: <Dict> of update request
        :returns: <Bool> of if request was added

        """
        if type(update) is dict:
            self._


class PageElement(object):

    """Initialized PageElement object and
    sets metadata properties and shared object
    operations.
    """

    def __init__(self, presentation, page, **kwargs):
        self._presentation = presentation
        self._page = page

        # initialize metadata
        self._id = kwargs.pop('objectId')
        self._size = kwargs.pop('size')
        self._transform = kwargs.pop('transform')
        self._title = kwargs.pop('title')
        self._description = kwargs.pop('description')


    def delete(self):
        """Adds deleteObject request to
        presentation updates list.
        """
        self._presentation.add_update({
            'deleteObject': dict(objectId=self._id)
        })


    def update(self, update):
        self._presentation.add_update(update)


class Table(PageElement):

    """Docstring for Table. """

    def __init__(self, **kwargs):
        """TODO: to be defined1.

        :table: dict w/ table object

        """
        table = kwargs.pop('table')
        self.rows, self.columns = table.get('rows'), table.get('columns')

        super(self.__class__, self).__init__(**kwargs)
