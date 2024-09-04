FROM python:3.12-slim

WORKDIR .

RUN pip install psycopg2-binary
RUN pip install telebot

COPY . .

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["bash", "-c"]
CMD ["./docker-entrypoint.sh"]
