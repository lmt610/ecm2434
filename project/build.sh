#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

#create example teams for the application 
python manage.py create_teams

#create example race entries for the application 
python manage.py create_race_entries