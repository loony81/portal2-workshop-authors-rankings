#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
echo $PG_PASSWORD
python manage.py my_command --username admin --password $PG_PASSWORD --email loonyonline@gmail.com