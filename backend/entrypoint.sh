#!/bin/sh

# Wait for the PostgreSQL database to be ready
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 3
done

# Create the PostGIS extension if it doesn't exist
echo "Creating PostGIS extension..."
python -c "
import os
import psycopg

# Connect to the database
conn = psycopg.connect(os.environ['DATABASE_URL'])
with conn:
    with conn.cursor() as cur:
        cur.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django application using gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
