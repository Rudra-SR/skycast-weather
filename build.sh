#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (for CSS/JS to work on the live site)
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate