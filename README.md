Kumbh Mela data entry interface
===============================

Started from 'Django tutorial' <https://docs.djangoproject.com/en/1.9/intro/>. See the tutorial for more information and for extending this example.

## Getting started

Make a virtualenv
```
pip install virtualenv
virtualenv kmenv
. kmenv/bin/activate
```
and install the requirements:
```
pip install -r requirements.txt
```

## How to use

The first time, make an admin
```
python manage.py createsuperuser
```

To start the web server, run
```
python manage.py runserver
```
It is only available on the current machine. Then enter data on <http://127.0.0.1/admin/>.

## How to modify 

Modify `entry/models.py` and `entry/admin.py` to adjust the database scheme. To get sensible names on the web interface for each object, be sure to implement a `__str__` function for all models.

After modification, run

```
python manage.py makemigrations entry
python manage.py sqlmigrate entry [number from previous command]
python manage.py migrate
python manage.py runserver
```

