#!/bin/sh
echo "Waiting for postgres..."

# scan the port to see whether postgres database is ready or not
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

python manage.py run_schedule
