import six

if six.PY3:
    builtins_open = 'builtins.open'
else:
    builtins_open = '__builtin__.open'
