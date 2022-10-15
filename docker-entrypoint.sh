#!/bin/bash

shopt -s histappend
# add check for checking if the mysql / redis services are up and accessible
./wait-for-it.sh db:5432

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
