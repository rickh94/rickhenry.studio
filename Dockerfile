FROM oven/bun:latest as builder1

WORKDIR /studioblog
COPY ./studioblog/package.json ./studioblog/bun.lockb .
RUN bun install
COPY ./studioblog/. .
RUN bun run build

FROM python:3.11-slim-bookworm

# RUN useradd wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
	PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install "gunicorn==20.0.4"
RUN pip install poetry

# Install the project requirements.
COPY pyproject.toml poetry.lock /
WORKDIR /
RUN poetry export -o requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

#RUN chown django:django /app

#COPY --chown=django:django ./app/. .
COPY ./studioblog/. .
COPY --from=builder1 /studioblog/studioblog/static/css/studioblog.css /app/studioblog/static/css/studioblog.css
#USER django

RUN python manage.py collectstatic --noinput --clear

CMD gunicorn studioblog.wsgi:application
