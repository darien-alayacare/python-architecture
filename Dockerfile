FROM python:3.9-slim-buster

COPY pyproject.toml .
RUN pip install poetry
RUN pip install flask
RUN poetry install

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code
ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run