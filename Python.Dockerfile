# https://hub.docker.com/repository/docker/bnnticketing/chatbox-base
# Usage: FROM bnnticketing/chatbox-base:1.0
FROM python:3.8-alpine

COPY ["./chatbox/requirements.txt", "/requirements.txt"]

RUN apk add build-base
ENV PYTHONUNBUFFERED 1

RUN pip install -r /requirements.txt