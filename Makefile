install:
	poetry install --no-root

lint:
	poetry run flake8 task_manager