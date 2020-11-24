#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python -m pip install --upgrade pip
#python manage.py collectstatic --no-input --clear
/usr/local/bin/python -m pip install --upgrade pip
celery -A exrate2020 worker -l info

exec "$@"