import unittest
from unittest import mock

from tests.utils import get_data
from google_objects.slides import SlidesClient
from google_objects.slides import Presentation
from google_objects.slides import Page
from google_objects.slides import PageElement

# load google sheets dummy data
presentation = get_data('presentation')

# initialize mock google-api-python-client resource object
mock_resource = mock.Mock()
mock_resource.presentations().get().execute.return_value = presentation


class TestDrive(unittest.TestCase):
    def setUp(self):
        self.client = SlidesClient(mock_resource)

    def test_presentation(self):
        presentation = self.client.get_presentation('abc123')
        self.assertIsInstance(presentation, Presentation)
        self.assertEqual(presentation.id, 'abc123')

    def test_pages(self):
        presentation = self.client.get_presentation('abc123')

        for slide in presentation.slides():
            self.assertIsInstance(slide, Page)
            self.assertIsNotNone(slide.id)

    def test_elements(self):
        presentation = self.client.get_presentation('abc123')

        for element in presentation.elements():
            self.assertIsInstance(element, PageElement)
            self.assertIsNotNone(element.id)
