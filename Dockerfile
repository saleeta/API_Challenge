FROM python:3.6.8-alpine

LABEL image for a very simple flask application

WORKDIR /the-shortest-url-1-kulvzv

COPY . /the-shortest-url-1-kulvzv

RUN ["pip", "install", "pipenv"]

RUN ["pipenv", "install"]

CMD pipenv install flask

CMD pipenv run python app.py