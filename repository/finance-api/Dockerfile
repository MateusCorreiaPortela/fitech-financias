FROM python:3.13

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8050", "--reload"]