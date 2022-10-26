FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN mkdir /app
COPY ./sklad /app
WORKDIR /app

RUN python -m pip install --upgrade pip  && \
    pip install pipenv && \
    pipenv sync

RUN apk del .tmp-build-deps
