FROM bnnticketing/chatbox-base:1.0

COPY ["./chatbox", "/chatbox"]

RUN /usr/bin/crontab /chatbox/crontab.txt
CMD ["crond", "-f"]

# ENTRYPOINT ["python3", "/chatbox/main.py"]
