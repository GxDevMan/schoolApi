FROM python:3

ENV DJANGOENV 1

WORKDIR /schoolApi

ADD . /schoolApi

COPY ./requirements.txt /schoolApi/requirements.txt

RUN pip install -r requirements.txt

COPY . /schoolApi