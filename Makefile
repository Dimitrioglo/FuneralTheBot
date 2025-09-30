
format:
	ruff format

lint:
	ruff check --fix

run:
	poetry run python src/app.py

install:
	poetry install
