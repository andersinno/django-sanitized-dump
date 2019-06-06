try:
    from ConfigParser import SafeConfigParser
except ImportError:  # pragma: no cover python 2 vs 3 issue
    from configparser import ConfigParser as SafeConfigParser

DATABASE_TYPES = ['mysql', 'postgres', 'postgis']


def get_database_engine_from_django_database(django_database):
    engine_module = django_database.get('ENGINE')
    engine = None
    for entry in DATABASE_TYPES:
        if entry in engine_module:
            engine = entry
            break
    return engine


def read_mysql_options_from_path(path):
    options = SafeConfigParser()
    options.read(path)
    keys = ["user", "password", "host", "port", "database"]
    result = {}
    for key in keys:
        if options.has_option("client", key):
            result[key] = options.get("client", key)
    return result


class DatabaseUrlBuilder(object):

    def __init__(self, engine, user, password, host, port, database):
        self.engine = engine
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def to_string(self):
        if not all([self.engine, self.database, self.host]):
            raise ValueError("Database configuration not supported")

        has_login = (self.user or self.password)

        login_part = '{user}:{password}@' if has_login else ''
        port_part = ':{port}' if self.port else ''

        database_string_template = (
            '{engine}://' + login_part + '{host}' + port_part + '/{db}')

        return database_string_template.format(
            engine=self.engine,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.database,
        )

    @classmethod
    def create_from_django_database(cls, django_database):
        engine = get_database_engine_from_django_database(django_database)
        if not engine:
            raise ValueError("Database configuration not supported")

        kwargs = {
            "engine": engine,
            "user": django_database.get("USER"),
            "password": django_database.get("PASSWORD"),
            "host": django_database.get("HOST", None) or "localhost",
            "port": django_database.get("PORT"),
            "database": django_database.get("NAME"),
        }

        if engine == "mysql":
            options = django_database.get("OPTIONS", {})
            options_path = options.get("read_default_file", None)
            if options_path:
                kwargs.update(read_mysql_options_from_path(options_path))

        return cls(**kwargs)


def db_setting_to_db_string(db_settings):
    default_db = db_settings.get('default')
    if not default_db:
        raise ValueError("No default database found")
    builder = DatabaseUrlBuilder.create_from_django_database(default_db)
    return builder.to_string()
