"""

Google Sliders Utility Functions
    Wed 14 Sep 10:57:00 2016

"""
import re
import os


def _find_credentials(name='xyz_creds.json'):
    """finds credentials within project

    :name: name of credential file
    :returns: full path to credentials

    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'lab/google-objects/.credentials')
    credential_path = os.path.join(credential_dir, name)
    return credential_path


def to_snake_case(name):
    temp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', temp).lower()


def to_camel_case(snake_str):
    snake_str = snake_str.lstrip('_')
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def keys_to_snake(dct):
    """turns all dictionary keys to snake case,
    adds leading underscore"""
    camel_keys = dct.keys()
    snake_keys = [to_snake_case(key) for key in camel_keys]

    for new, old in zip(snake_keys, camel_keys):
        # transform camel keys to private snake keys
        dct['_{}'.format(new)] = dct.pop(old)

    return dct

def keys_to_camel(dct):
    """turns all dictionary keys to camel case"""
    snake_keys = dct.keys()
    camel_keys = [to_camel_case(key) for key in snake_keys]

    for new, old in zip(camel_keys, snake_keys):
        # transform camel keys to private snake keys
        dct[new.lstrip('_')] = dct.pop(old)

    return dct



class DELETE_MODES:
    DELETE_ALL = 'DELETE_ALL'


class SlidesUpdate(object):
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
