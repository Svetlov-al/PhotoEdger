FROM python:3.11-slim-buster

# RUN apt install gcc libpq (no longer needed bc we use psycopg2-binary)
RUN apt-get update && apt-get install -y fonts-dejavu-core

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
RUN mkdir -p /image_files

COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
