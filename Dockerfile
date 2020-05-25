FROM python:3.8

RUN apt-get update
RUN apt-get -y install \
    tesseract-ocr
RUN apt-get clean

WORKDIR /script

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv sync

COPY . .
