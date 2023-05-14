#!/bin/sh
pip install git+https://${GITHUB_TOKEN}@github.com/ridwanray/micro_shared_lib.git@main
python manage.py makemigrations --no-input
python manage.py migrate --no-input
rm celerybeat.pid

exec "$@"