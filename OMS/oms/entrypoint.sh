#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Apply database migrations
python manage.py migrate

# Apply create superuser
python manage.py createsuperuser

# Run Django server
python manage.py runserver 0.0.0.0:80

# Run the Django server
exec "$@"
