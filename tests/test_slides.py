import os
import pytest

from google_objects import SlidesAPI
from google_objects.slides import Presentation, Page
from google_objects.slides import PageElement, Shape, Table
from google_objects.slides import TextContent


@pytest.fixture
def client(credentials):
    api = SlidesAPI(credentials)
    return api


def test_get_presentation(client):
    test_presentation = os.getenv('TEST_PRESENTATION')
    presentation = client.get_presentation(test_presentation)
    assert isinstance(presentation, Presentation)


def test_get_page(client):
    test_presentation = os.getenv('TEST_PRESENTATION')
    page_id = os.getenv('PAGE')
    page = client.get_page(test_presentation, page_id)
    assert isinstance(page, Page)


@pytest.fixture
def presentation(client):
    test_presentation = os.getenv('TEST_PRESENTATION')
    return client.get_presentation(test_presentation)


def test_elements(presentation):
    for page in presentation:
        assert isinstance(page, Page)
        for element in page:
            assert isinstance(element, PageElement)
            if isinstance(element, Table):
                for cell in element.cells():
                    assert isinstance(cell.text, TextContent)
                    if '_text' in vars(cell):
                        for text in cell.text:
                            text = cell.text
                        for piece in text:
                            assert piece.end_index > 0

            if isinstance(element, Shape):
                if '_text' in vars(element):
                    text = element.text
                    assert isinstance(text, TextContent)
                    for piece in text:
                        assert piece.end_index > 0


def test_get_matches(presentation):
    regex = os.getenv('REGEX')

    with presentation:
        tags = presentation.get_matches(regex)
        for i, tag in enumerate(tags):
            text, info = tag
            presentation.replace_text(text, i)
        # for i, tag in enumerate(tags):
