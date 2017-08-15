def DELETE_OBJECT(obj_id):
    return {
        'deleteObject': {
            'objectId': obj_id
        }
    }


def REPLACE_ALL_TEXT(find, replace, case_sensitive=False):
    return {
        'replaceAllText': {
            'replaceText': replace,
            'containsText': {
                'text': find,
                'matchCase': case_sensitive
            }
        }
    }


def INSERT_TEXT(text, obj_id=None, row=None, column=None, start=0):
    return {
        'insertText': {
            'objectId': obj_id,
            'text': text,
            'cellLocation': {
                'rowIndex': row,
                'columnIndex': column
            },
            'insertionIndex': start

        }
    }


def DELETE_TEXT(obj_id, row=None,
                col=None, start=None, end=None, kind='FIXED_RANGE'):
    return {
        'deleteText': {
            'objectId': obj_id,
            'cellLocation': {
                'rowIndex': row,
                'columnIndex': col
            },
            'text_range': {
                'startIndex': start,
                'endIndex': end

            },
        }
    }
