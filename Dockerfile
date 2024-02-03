FROM ubuntu:20.04

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip postgresql postgresql-contrib redis-server && \
    pip3 install -r requirements.txt

ENV NAME World

CMD ["python3", "app.py"]

