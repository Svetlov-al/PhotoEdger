FROM python:3.11-alpine

# RUN apt install gcc libpq (no longer needed bc we use psycopg2-binary)
RUN apk add --no-cache \
    sqlite \
    sqlite-dev \
    fontconfig \
    ttf-dejavu

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
RUN mkdir -p /image_files

COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
