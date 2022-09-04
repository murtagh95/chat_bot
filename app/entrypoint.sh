#!/bin/sh

echo "Waiting for postgres..."
echo "$POSTGRES_HOST"
echo "$POSTGRES_PORT"
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Using gunicorn"
exec uvicorn $APP_MODULE --host 0.0.0.0 --reload

