"""

Google Sliders Utility Functions
    Wed 14 Sep 10:57:00 2016

"""
import re


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


def keys_to_snake(dt):
    """changes camel_cased keys on argument to
    snake case"""

    camel_keys = dt.keys()
    snake_keys = [to_snake_case(key) for key in camel_keys]

    for new, old in zip(snake_keys, camel_keys):
        # transform camel keys to private snake keys
        dt[new] = dt.pop(old)

    return dt


def keys_to_camel(dct):
    """changes snake_cased keys on argument to
    camel_case"""

    snake_keys = dct.keys()
    camel_keys = [to_camel_case(key) for key in snake_keys]

    for new, old in zip(camel_keys, snake_keys):
        # transform camel keys to private snake keys
        dct[new.lstrip('_')] = dct.pop(old)

    return dct
