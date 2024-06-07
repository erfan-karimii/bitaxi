#!/bin/sh

set -e

cd /app/

echo 'Collecting static files...'
python3 manage-production.py collectstatic --no-input

echo 'Running migrations...'
python3 manage-production.py migrate --no-input

echo 'Running server...'
gunicorn core.wsgi --bind 0.0.0.0:8000