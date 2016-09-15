"""

Google Sliders Utility Functions
    Wed 14 Sep 10:57:00 2016

"""
import os


def _find_credentials(name='xyz_creds.json'):
    """finds credentials within project

    :name: name of credential file
    :returns: full path to credentials

    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'lab/google-sliders/.credentials')
    credential_path = os.path.join(credential_dir, name)
    return credential_path


class DELETE_MODES:
    DELETE_ALL = 'DELETE_ALL'


class UpdateReq(object):
    """Update Operations <Dicts> for Presentations"""

    @staticmethod
    def delete_object(obj_id):
        return {
            'deleteObject': {
                'objectId': obj_id
            }
        }

    @staticmethod
    def replace_all_text(find, replace, case_sensitive=False):
        return {
            'replaceAllText': {
                'findText': find,
                'replaceText': replace,
                'matchCase': case_sensitive
            }
        }

    @staticmethod
    def insert_text(obj_id, text, row=None, column=None, insertion_index=0):
        return {
            'insertText': {
                'objectId': obj_id,
                'text': text,
                'cellLocation': {
                    'rowIndex': row,
                    'columnIndex': column
                },
                'insertionIndex': insertion_index

            }
        }
        pass

    @staticmethod
    def delete_text(obj_id, row=None, column=None, mode='DELETE_ALL'):
        return {
            'deleteText': {
                'objectId': obj_id,
                'cellLocation': {
                    'rowIndex': row,
                    'columnIndex': column
                },
                'deleteMode': mode
            }
        }
