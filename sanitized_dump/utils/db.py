DATABASE_TYPES = ['mysql', 'postgres']
DATABASE_STRING_TEMPLATE = '{type}://{username}:{password}@{host}:{port}/{db}'
DEFAULT_DATABASE_PORTS = {
    'mysql': '3306',
    'postgres': '5432',
}


def db_setting_to_db_string(db_settings):
    default_db = db_settings.get('default')

    if not default_db:
        raise ValueError("No default database found")

    engine = default_db.get('ENGINE')
    db_name = default_db.get('NAME')
    db_user = default_db.get('USER')
    db_password = default_db.get('PASSWORD')
    db_host = default_db.get('HOST')
    db_port = default_db.get('PORT')

    if not (engine and db_name and db_user and db_host):
        raise ValueError("Database configuration not supported")

    database_type = None
    for db_type in DATABASE_TYPES:
        if db_type in engine:
            database_type = db_type
            break

    if not database_type:
        raise ValueError('Database type "{}" is not supported'.format(engine))

    # Use default port if no port is set
    db_port = db_port if db_port else DEFAULT_DATABASE_PORTS[database_type]

    return DATABASE_STRING_TEMPLATE.format(
        type=database_type,
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        db=db_name,
    )
