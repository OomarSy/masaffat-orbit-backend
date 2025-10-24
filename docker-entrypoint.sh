#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# # Apply Partitioning
# echo "Apply Partitioning"
# python manage.py pgpartition -y

# Cache Tables
echo "Creating cache table"
python manage.py createcachetable

# compil messages
# echo "Compileng Messages Translation"
# python manage.py compilemessages

# Super User
echo "Creating superuser"
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL 
fi

$@

# Start server
echo "Starting server"
daphne --bind 0.0.0.0 --port 8080 --http-timeout 300 config.asgi:application