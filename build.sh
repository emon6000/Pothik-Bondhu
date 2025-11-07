#!/usr/bin/env bash
# This script tells Render what to do

# Exit on error
set -o errexit

# Install all our packages
pip install -r requirements.txt

# Run the database 'setup'
python manage.py migrate

# Load our 64 districts into the new database
python manage.py loaddata districts