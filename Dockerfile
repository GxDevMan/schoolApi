FROM python:3

ENV DJANGOENV 1

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR /schoolApi

COPY . .
