PORT ?= 8000

dev:
	poetry run python manage.py runserver

start:
	poetry run python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

build:
	./build.sh

install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

test-cov:
	poetry run coverage run manage.py test
	poetry run coverage xml

dev-cov:
	poetry run coverage run manage.py test
	poetry run coverage report -m