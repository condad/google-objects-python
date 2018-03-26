# -*- coding: utf-8 -*-
import logging

# sets default logging handler to avoid "No handler found" warnings.
try:
    # for Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

from .drive import DriveClient
from .sheets import SheetsClient
from .slides import SlidesClient
