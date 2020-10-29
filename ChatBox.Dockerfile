FROM python:3.8-alpine

COPY ["./chatbox", "/chatbox"]

RUN apk add build-base
RUN pip install -r /chatbox/requirements.txt

ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["python3", "/chatbox/main.py"]
