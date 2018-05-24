DATABASE_TYPES = ['mysql', 'postgres', 'postgis']


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

    if not engine or not db_name:
        raise ValueError("Database configuration not supported")

    database_type = None
    for db_type in DATABASE_TYPES:
        if db_type in engine:
            database_type = db_type
            break

    if not database_type:
        raise ValueError('Database type "{}" is not supported'.format(engine))

    login_part = '{username}:{password}@' if (db_user or db_password) else ''
    port_part = ':{port}' if db_port else ''
    database_string_template = (
        '{type}://' + login_part + '{host}' + port_part + '/{db}')

    return database_string_template.format(
        type=database_type,
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        db=db_name,
    )
