niko-niko
=========

The main idea is to have a web form available for one vote over three smileys in order to know their mood.

Requirements
------------

You will need `pip`.

Set up
------

### Development

You should [install virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html). Then set up goes down to:

```sh
$ mkvirtualenv niko -p /usr/bin/python2.7 -a /w/niko_niko -r devrequirements
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
    execfile(settings_local_file)
```

### Production

```sh
$ pip install -r requirements
```
Edit `niko_niko/settings.py`, at the end, remove:

```python
settings_local_file = os.path.join(BASE_DIR, 'settings_local.py')
if os.path.exists(settings_local_file):
    execfile(settings_local_file)
```

### For All

Here are the useful settings:

```python
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

Now create database:

```sh
$ python manage.py syncdb
```

Run
---

After a `$ python manage.py runserver_plus`, you will able to visit `http://localhost:8000/`.

If you want fill it, try:

```sh
$ python manage.py loaddata data/sample.json
```
