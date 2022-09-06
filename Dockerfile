FROM python:3.10.6-alpine

WORKDIR '/app'
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Update and install dependecies os
RUN apk update && apk add gcc build-base
RUN apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev
RUN apk add --no-cache --virtual .build-deps g++ python3-dev py3-setuptools libffi-dev openssl-dev && \
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
