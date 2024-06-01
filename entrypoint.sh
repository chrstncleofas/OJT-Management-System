#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Run the Django server
exec "$@"
