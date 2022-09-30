FROM python:latest

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install -r /usr/src/app/requirements.txt

CMD python /usr/src/app/main.py
