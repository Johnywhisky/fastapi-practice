FROM python:3.11.0-buster

ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV  \
   && $POETRY_VENV/bin/pip install -U pip setuptools \
   && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /project/

COPY . .
RUN poetry install --only main

EXPOSE 8080
CMD ["poetry", "run", "gunicorn", "-c", "gunicorn.conf.py", "src.main:app"]
