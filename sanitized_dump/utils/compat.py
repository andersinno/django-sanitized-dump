import six

if six.PY3:
    builtins_open = 'builtins.open'
else:
    builtins_open = '__builtin__.open'


def deunicode(item):
    """ Convert unicode objects to str """
    if item is None:
        return None
    if isinstance(item, str):
        return item
    if isinstance(item, six.text_type):
        return item.encode('utf-8')
    if isinstance(item, dict):
        return {
            deunicode(key): deunicode(value)
            for (key, value) in item.items()
        }
    if isinstance(item, list):
        return [deunicode(x) for x in item]
    raise TypeError('Unhandled item type: {!r}'.format(item))
