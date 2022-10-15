#!/bin/bash

shopt -s histappend
# add check for checking if the mysql / redis services are up and accessible
./wait-for-it.sh db:5432

pip install -r requirements/test.txt

# Start server
echo "Starting server"
./manage.py test  --settings=octoenergy.test_settings --failfast

