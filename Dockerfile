FROM python:3.10.6-alpine

RUN mkdir /app
WORKDIR /app

ADD .env /app/.env
ADD config.json /app/config.json
ADD app.py /app/app.py
ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN addgroup -S 1337 && adduser -S 1337 -G 1337
USER 1337

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]