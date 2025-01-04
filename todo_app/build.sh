#!/usr/bin/env bash
# Exit on error
set -e errexit

# Install dependencies
pip3 install -r requirements.txt

# convert static asset files
python3 manage.py collectstatic --no-input

# Apply database migrations
python3 manage.py migrate
