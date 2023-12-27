#!/bin/bash

cd /innoter_drf/backend

python manage.py migrate

python manage.py runserver 0.0.0.0:8001
