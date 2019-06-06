from tempfile import NamedTemporaryFile

import pytest

from sanitized_dump.utils.db import db_setting_to_db_string


@pytest.mark.parametrize("engine, name, user, password, host, port, expected", [
    ("django.db.backends.mysql", "db", "user", "password", "host", "3306",
        "mysql://user:password@host:3306/db"),
    ("django.db.backends.mysql", "db", "user", "password", "host", "3307",
        "mysql://user:password@host:3307/db"),
    ("django.db.backends.mysql", "db", "user", "password", None, None,
        "mysql://user:password@localhost/db"),
    ("django.db.backends.postgresql", "db", "user", "password", None, None,
        "postgres://user:password@localhost/db"),
    ("django.db.backends.postgresql", "db", "user", "password", None, 1111,
        "postgres://user:password@localhost:1111/db"),
    ("django.contrib.gis.db.backends.postgis", "johannes", "hernekeitto", "viina", "teline", 1111,
        "postgis://hernekeitto:viina@teline:1111/johannes"),
])
def test_db_url_generation(engine, name, user, password, host, port, expected):
    databases = {
        "default": {
            "ENGINE": engine,
            "NAME": name,
            "USER": user,
            "PASSWORD": password,
            "HOST": host,
            "PORT": port,
        }
    }

    result = db_setting_to_db_string(databases)
    assert result == expected


@pytest.mark.parametrize("database, user, password, host, port, expected", [
    ("db", "user", "password", "host", 3306, "mysql://user:password@host:3306/db"),
    ("db", "user", "password", "host", 3307, "mysql://user:password@host:3307/db"),
    ("db", "user", "password", None, None, "mysql://user:password@localhost/db"),
    ("db", "user", "password", None, 5432, "mysql://user:password@localhost:5432/db"),
    ("db", "user", "password", None, 1111, "mysql://user:password@localhost:1111/db"),
    ("johannes", "hernekeitto", "viina", "teline", 1111, "mysql://hernekeitto:viina@teline:1111/johannes"),
])
def test_mysql_options_file_reading(database, user, password, host, port, expected):
    config_lines = ["[client]"]
    params = dict(database=database, user=user, password=password, host=host, port=port)
    for key, value in params.items():
        if value:
            config_lines.append("%s=%s" % (key, value))

    with NamedTemporaryFile(delete=False) as f:
        f.write(("\n".join(config_lines)).encode("utf-8"))
        f.flush()
        databases = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "OPTIONS": {
                    "read_default_file": f.name,
                },
            }
        }
        result = db_setting_to_db_string(databases)
        assert result == expected
