niko-niko
=========

The main idea is to have a web form available for one vote over three smileys in order to know their mood.

Requirements
------------

Made with:
* `pip` > 8.0
* `python` > 3.5

Set up
------

### Development

You should [install virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html). Then set up goes down to:

```sh
$ mkvirtualenv niko -p /usr/bin/python3 -a /w/niko_niko -r devrequirements
$ workon niko
```

__Note__: Note adjust path used for `mkvirtualenv` to your system.

Now you just need to adjust some settings. At the root of the project run:

```sh
$ cp niko_niko/settings.py niko_niko/settings_local.py
```

Edit `niko_niko/settings_local.py`, at the end, remove:

```python
settings_local_file = os.path.join(BASE_DIR, 'settings_local.py')
if os.path.exists(settings_local_file):
    with open(settings_local_file) as local_configuration:
        code = compile(local_configuration.read(), local_configuration, "exec")
        exec(code)
```

### Production

```sh
$ pip install -r requirements
```
Edit `niko_niko/settings.py`, at the end, remove:

```python
settings_local_file = os.path.join(BASE_DIR, 'settings_local.py')
if os.path.exists(settings_local_file):
    with open(settings_local_file) as local_configuration:
        code = compile(local_configuration.read(), local_configuration, "exec")
        exec(code)
```

### For All

Here are the useful settings:

```python
# Base of links in QR codes :)
ALLOWED_HOSTS = ['18.34.88.76:8000']
# Set yourself as admin
ADMINS = (
    ('Kevin KIN-FOO', 'ken@cap.com'),
)
# Define dev database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/path/to/niko_niko/data/db.sq3', # Path, as we are using sqlite3.
    }
}
```

Now create database and enable admin material:

```sh
$ python manage.py syncdb
$ python manage.py collectstatic
```

Run
---

After a `$ python manage.py runserver 0.0.0.0:8000`, you will able to visit `http://localhost:8000/`.

If you want fill it, try:

```sh
$ python manage.py loaddata data/sample.json
```

Troubleshooting
---------------

### QR codes: Unable to connect

Did you start application with: `$ python manage.py runserver 0.0.0.0:8000`?

Because default `runserver` sub-command only works for `localhost`.
