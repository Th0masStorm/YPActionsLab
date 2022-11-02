FROM python:3-slim

WORKDIR /app

ADD requirements.txt /app/requirements.txt
ADD main.py /app/main.py

RUN pip install -r /app/requirements.txt

EXPOSE 5000
CMD [ "/app/main.py" ]