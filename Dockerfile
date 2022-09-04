FROM python:3.10.6-alpine

WORKDIR '/app'
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Update and install dependecies os
RUN apk update && apk add gcc build-base
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./poetry.lock /app
COPY ./pyproject.toml /app

# for poetry
RUN poetry install -n

ARG APP_PORT
ARG APP_HOST
ARG APP_MODULE

COPY ./app /app
