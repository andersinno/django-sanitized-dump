# django-sanitized-dump
Sanitize sensitive information from your database dumps 💩

Supports:
- PostgreSQL
- MySQL

# Getting started

1. `pip install django-sanitized-dump` or `pip install django-sanitized-dump[MySQL]` if you use MySQL
2. Add `sanitized_dump` to `INSTALLED_APPS`
3. Initialize config file: `./manage.py init_sanitizer`
4. Check your newly created `.sanitizerconfig` file and modify the sanitation strategy to fit your requirements.
5. Run `./manage.py check_sanitizerconfig` to verify that your `.sanitizerconfig` includes all models and fields
6. Get sanitized database dump: `./manage.py create_sanitized_dump > dump.sql`

# DB Sanitation

Heavy lifting of the DB sanitation is done by: https://github.com/andersinno/python-database-sanitizer

### Configuration

Configuration file is used to define a strategy on how to sanitize your data. Strategy defines a sanitation function for each model field.

#### Example config
```yaml
config:
 addons:
   - "ai-sanitizers"
   - "some-other-lib"
strategy:
 user:
   first_name: "name.first_name"
   last_name: "name.last_name"
 education:
   created: null
   modified: null
   id: null
   field: "education.field"
   school: "education.school"
   started: "datetime.datetime"
   credits: null
   information: "string.loremipsum_preserved"
 file_file: null
```

#### Example custom sanitizers
```python
# /sanitizers/name.py
def sanitize_first_name(value):
    return faker.first_name()

def sanitize_last_name(value):
    return faker.last_name()

# /sanitizers/education.py
def sanitize_field(value):
    return "Some field"

def sanitize_schoo(value):
    return "My school"
```

#### Validating sanitizer return value

> Note: This should not be done in the initial implementation of the sanitizer but is up to the sanitizer functions. This is just a nice to have but not of a high priority.

Check that the returned value is of the same type as the argument value passed to the sanitizer.
For instance, if a MySQL DATETIME value is passed to the sanitizer, a MySQL DATETIME value shoud be returned as well.


#### Configuration method resolution order

1. Custom sanitizers inside ./sanitizers
2. Addon sanitizers (`config.addons`)
3. Core sanitizers

### Django Management Commands

#### Sanitized Dump

`./manage.py create_sanitized_dump > dump.sql`

1. Warn about unhandled fields
2. Creates a database dump (`mysqldump`/`pgdump`)
3. Run sanitizer


#### Check Sanitized Dump

`./manage.py check_sanitizerconfig`

1. Returns an error code if there are unhandled database fields

Check can be used in CI environments for detecting changes in models, that are not present in
sanitizer configuration.


#### Init Sanitizer

`./manage.py init_sanitizer`

1. Create configuration from current database state
