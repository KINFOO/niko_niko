niko-niko
=========

The main idea is to have a web form available for one vote over three smileys in order to know their mood.

Requirements
------------

You will need `pip`.

Set up
------

You should [install virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html). Then set up goes down to:

```sh
$ mkvirtualenv niko -p /usr/bin/python2.7 -a /w/niko_niko -r requirements -r requirementsDev
$ workon niko
```
__Note__: Note adjust path used for `mkvirtualenv` to your system.

Now you just need to adjust some settings. At the root of the project run:

```sh
$ cp niko_niko/settings.py settings_local.py
```

Edit `settings_local.py`:
```python
# Set yourself as admin
ADMINS = (
    ('Kevin KIN-FOO', 'ken@cap.com'),
)
# Define dev database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/path/to/niko_niko/db.sq3',          # Path as we are using sqlite3.
    }
}
# Ensure admin is defined
INSTALLED_APPS = (
    # 'django.contrib' ya di ya da
    # ...
    # Uncomment the next line to enable the admin:
    'django.contrib.admin', # Here you go
    # ...
    # Define the app we are coding
    'niko'
)
```

Now create database:
```sh
$ python manage.py syncdb
```

Run
---

After a `$ python manage.py runserver`, you will able to visit `http://localhost:8000/`.

If you want fill it, try:
```sh
$ python manage.py loaddata data/sample.json
```
