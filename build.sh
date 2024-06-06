#!/usr/bin/env bash
# exit on error
set -o errexit

export DJANGO_SETTINGS_MODULE=mysite.settings

# change this line for whichever package you use, such as pip, or poetry, etc.
pip install -r requirements.txt

# convert our static asset files on Render
python manage.py collectstatic --no-input

# apply any database migrations that are outstanding
python manage.py makemigrations
python manage.py migrate

python manage.py createsu

python render/pedrao-imoveis.py
python render/defranco-imoveis.py



