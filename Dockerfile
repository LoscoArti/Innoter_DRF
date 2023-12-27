FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /backend:$PYTHONPATH

RUN mkdir /innoter_drf

COPY poetry.lock pyproject.toml ./

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN pip install poetry==1.7.0

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . ./

CMD ["./entrypoint.sh"]
