#!/usr/bin/env python
import sys
from os import path, environ

import django
import py
from django.conf import settings

# Give feedback on used versions
sys.stderr.write('Using Python version {0} from {1}\n'.format(sys.version[:5], sys.executable))
sys.stderr.write('Using Django version {0} from {1}\n'.format(
    django.get_version(),
    path.dirname(path.abspath(django.__file__)))
)

if not settings.configured:
    module_root = path.dirname(path.realpath(__file__))
    sys.path.insert(0, path.join(module_root, 'tests'))
    sys.path.insert(0, module_root)
    environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

DEFAULT_TEST_APPS = [
    'tests',
]


def runtests():
    other_args = list(filter(lambda arg: arg.startswith('-'), sys.argv[1:]))
    test_apps = list(filter(lambda arg: not arg.startswith('-'), sys.argv[1:])) or DEFAULT_TEST_APPS

    argv = sys.argv[:1] + other_args + test_apps
    sys.exit(py.test.cmdline.main(argv))


if __name__ == '__main__':
    runtests()
