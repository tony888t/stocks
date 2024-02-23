#!/bin/sh

echo "Running Migrations"
poetry run python manage.py migrate --no-input

exec "$@"
