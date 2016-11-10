"""

Google Sliders Utility Functions
    Wed 14 Sep 10:57:00 2016

"""

import re
from functools import wraps


def handle_key_error(func):
    @wraps(func)
    def func_wrapper(self):
        try:
            return func(self)
        except KeyError:
            return
    return func_wrapper


def set_private_attrs(instance, dt):
    """Sets (key, value) pairs of given dictionary
    to private attributes (single leading underscore).

    :instance: <Objec> Instance
    :dt: <Dict>

    """

    for key, val in dt.iteritems():
        setattr(instance, '_{}'.format(key), val)
        # self.__dict__['_{}'.format(key)] = val


def to_snake_case(string):
    """changes camel_cased strings to snake_case"""

    temp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', temp).lower()


def to_camel_case(string):
    """changes snake_cased strings to camel cases,
    strips leading underscores
    """

    components = string.lstrip('_').split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def list_to_snake(a):
    newArr = []

    for i in a:
        if isinstance(i, list):
            newArr.append(list_to_snake(i))
        elif isinstance(i, dict):
            newArr.append(keys_to_snake(i))
        else:
            newArr.append(i)

    return newArr


def keys_to_snake(dt):
    """recursively changes camel_cased keys on argument to
    snake case"""

    for key, val in dt.iteritems():
        if isinstance(val, list):
            val = list_to_snake(val)

        if isinstance(val, dict):
            val = keys_to_snake(val)

        new_key = to_snake_case(key)
        dt[new_key] = dt.pop(key)

    return dt


def keys_to_camel(dt):
    """recursively changes snake_cased keys on argument to
    camel_case, strips leading underscores"""

    for key, val in dt.iteritems():
        if isinstance(val, dict):
            val = keys_to_camel(val)

        new_key = to_camel_case(key).lstrip('_')
        dt[new_key] = dt.pop(key)

    return dt
