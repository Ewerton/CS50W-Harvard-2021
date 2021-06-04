#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

# Apply database migrations
echo "Make database migrations (if any)"
python3 manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate --noinput || exit 1 # de erro, para a inicialização do container retornando 1 para o S.O

#Creating the superuser
echo "Creating superuser"
python3 manage.py createsuperuser --noinput
# Talvez seja melhor criar um comando personalizado para o manage.py  https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/

# Start server (The CMD of the dockerfile will call the runserver)
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000