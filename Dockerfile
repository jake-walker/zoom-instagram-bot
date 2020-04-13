FROM python:3.7-alpine

LABEL com.centurylinklabs.watchtower.enable="true"

ADD . /app
WORKDIR /app

RUN apk add --no-cache git
RUN pip install --upgrade pip pipenv
RUN pipenv install --system

ENV BOT_USERNAME "changeme"
ENV BOT_PASSWORD "changeme"

CMD ["python", "bot.py"]
