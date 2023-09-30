FROM python:3.10-slim

WORKDIR /parabible

RUN apt -y update
RUN apt -y install libpq-dev \
&& apt -y install python3-dev \
&& apt -y install build-essential

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "uwsgi", \
"--http", "0.0.0.0:5000", \
"--wsgi-file", "run.py", \
"--callable", "app", \
"--processes", "1", "--threads", "2", \
"--stats", "127.0.0.1:9191" ]
