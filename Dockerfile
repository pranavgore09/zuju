from python:3.8

# I was facing an issue where logs were not appearing in Docker-logs until I restart the server
# Do not buffer the stdout - asap
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
COPY requirements/ requirements/

RUN pip install -r requirements.txt
RUN pip install -r requirements/dev.txt
RUN pip install -r requirements/test.txt

EXPOSE 8000


