FROM python:3.8

WORKDIR /script

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv sync

COPY . .
