niko-niko
=========

The main idea is to have a web form available for one vote over three smileys in order to know their mood.

Requirements
------------

You will need `pip`

Set up
------

Install `virtualenv`:

```sh
$ pip install --user virtualenv
```

Create one for current project:
```sh
$ cd /path/to/niko_niko
$ virtualenv .
```

Enter your `virtualenv`:
```sh
$ source bin/activate
```

Use it to install what is needed:
```sh
$ pip install -r requirements
```

Edit `niko_niko/settings.py`:
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

__Note__: If it does not work, ensure your `virtualenv` is activated with: `$ source bin/activate`.

if you want fill it, try;
```sh
$ python manage.py loaddata data/sample.json
```
