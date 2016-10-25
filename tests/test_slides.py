import os
import pytest

from google_objects import SlidesAPI
from google_objects.slides import Presentation, Page


@pytest.fixture
def client(credentials):
    api_key = os.getenv('API_KEY')
    api = SlidesAPI(credentials, api_key)
    return api


@pytest.fixture
def presentation(client):
    test_presentation = os.getenv('TEST_PRESENTATION')
    return client.get_presentation(test_presentation)


def test_get_presentation(presentation):
    assert isinstance(presentation, Presentation)


def test_get_page(client):
    test_presentation = os.getenv('TEST_PRESENTATION')
    page_id = os.getenv('PAGE')
    page = client.get_page(test_presentation, page_id)
    assert isinstance(page, Page)


def test_get_matches(presentation):
    regex = os.getenv('REGEX')

    with presentation:
        tags = presentation.get_matches(regex)
        # print len(tags) + 'tags'
        for i, tag in enumerate(tags):
            presentation.replace_text(tag, i)
