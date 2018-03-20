# django-sanitized-dump
Sanitized sensitive information from your database dumps 💩


# DB Sanitization

### Configuration


#### Example config
```yaml
config:
 addons:
   - "ai-senitizers"
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
def sanitize_field(value):""
	return "Some field"

def sanitize_schoo(value):
    return "My school"
```

#### Validating sanitizer return value

> Note: This should not be done in the initial implementation of the sanitizer but is up to the sanitizer funtions. This is just a nice to have but not of a high priority.

Check that the returned value is of the same type as the argument value passed to the sanitizer.
For instance, if a MySQL DATETIME value is passed to the sanitizer, a MySQL DATETIME value shoud be returned as well.



#### Configuration method resolution order

1. Custom sanitizers inside ./sanitizers
2. Addon sanitizers (`config.addons`)
3. Core sanitizers



### Django Management Commands

#### Sanitized Dump

`./manage.py sanitized_dump -c > dump.sql`

1. Warn about unhandled fields
2. Creates a database dump (`mysqldump`/`pgdump`)
3. Run sanitazier


#### Check Sanitize Dump

`./manage.py sanitized_dump -c`

1. Returns an error code if there are unhandled database fields


#### Init Sanitizer

`./manage.py init_sanitizer`

1. Create configuration from current database state
