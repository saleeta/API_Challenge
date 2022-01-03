FROM python:3.6.8-alpine

RUN apk add --no-cache python3-dev \
    && pip install --upgrade pip

WORKDIR ./the-shortest-url-1-kulvzv

COPY ./requirements.txt /the-shortest-url-1-kulvzv/requirements.txt

RUN pip install -r requirements.txt

COPY . /the-shortest-url-1-kulvzv

EXPOSE 5000

ENTRYPOINT FLASK_APP=/the-shortest-url-1-kulvzv/app.py flask run --host=0.0.0.0