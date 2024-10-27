#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

make start
python manage.py migrate