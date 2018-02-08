import unittest
from unittest import mock

from tests.utils import get_data
from google_objects.drive import DriveClient
from google_objects.drive import About
from google_objects.drive import File
from google_objects.drive import Permission

# load google sheets dummy data
about = get_data('about')
get_file = get_data('get_file')
copy_file = get_data('copy_file')
permission = get_data('permission')

# initialize mock google-api-python-client resource object
mock_resource = mock.Mock()
mock_resource.about().get().execute.return_value = about
mock_resource.files().get().execute.return_value = get_file
mock_resource.files().copy().execute.return_value = copy_file
mock_resource.permissions().create().execute.return_value = permission


class TestDrive(unittest.TestCase):
    """Test Google Sheets objects"""

    def setUp(self):
        self.client = DriveClient(mock_resource)

    def test_about(self):
        about = self.client.get_about('abc123')
        self.assertIsInstance(about, About)

        self.assertEqual(about.name, 'Test User')
        self.assertEqual(about.email, 'test@gmail.com')
        self.assertEqual(about.permission_id, '1234')
    
    def test_get_file(self):
        gfile = self.client.get_file('abc123')
        self.assertIsInstance(gfile, File)

        self.assertEqual(gfile.id, 'abc123')
        self.assertEqual(gfile.name, 'Test File')
        self.assertEqual(gfile.type, 'application/vnd.google-apps.document')

        self.assertIn('p1', gfile.parents)
        self.assertIn('p2', gfile.parents)
        self.assertIn('p3', gfile.parents)

    def test_copy_file(self):
        gfile = self.client.copy_file('abc123')
        self.assertIsInstance(gfile, File)

        self.assertEqual(gfile.name, 'Copy of Test File')
        self.assertEqual(gfile.type, 'application/vnd.google-apps.document')

    def test_permission(self):
        gfile = self.client.get_file('abc123')

        for permission in gfile.permissions():
            self.assertIsInstance(permission, Permission)

        permission = gfile.add_permission('test@gmail.com', role='reader')
        self.assertEqual(permission.id, 'abc123')
        self.assertEqual(permission.type, 'user')
        self.assertEqual(permission.email, 'test@gmail.com')
        self.assertEqual(permission.role, 'reader')
