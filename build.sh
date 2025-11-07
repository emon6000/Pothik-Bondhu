#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

# --- THIS IS THE NEW, CRITICAL LINE ---
python manage.py collectstatic --no-input
# --- END OF FIX ---

python manage.py migrate
python manage.py loaddata districts