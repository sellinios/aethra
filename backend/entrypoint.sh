#!/bin/sh

# Wait for the PostgreSQL database to be ready
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 3
done

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django application using gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
