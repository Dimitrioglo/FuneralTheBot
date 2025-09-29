
format:
	ruff check --fix

lint:
	ruff check

run:
	poetry run python src/app.py

install:
	poetry install
