FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
 && poetry install --without dev --no-interaction --no-ansi

COPY . .

CMD ["python", "src/app.py"]
