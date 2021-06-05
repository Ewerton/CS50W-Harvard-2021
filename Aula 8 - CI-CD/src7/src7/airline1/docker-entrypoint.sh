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
#echo "Creating superuser"
# COmentei pois criei empty migration no projeto users e nesta migration crio o superuser 
# usando os valores definidos em variáveis de ambinete definidas no docker compose
#python3 manage.py createsuperuser --noinput


# Start server (The CMD of the dockerfile will call the runserver)
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000