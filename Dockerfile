FROM python:3.12

RUN pip install requests flask
ENV PYTHONPATH=/srv
