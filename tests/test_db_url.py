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
