#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

make dev
# python manage.py migrate