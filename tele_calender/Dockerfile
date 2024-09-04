FROM python:3.12-slim

WORKDIR tele_calender/

RUN pip install Django
RUN pip install psycopg2-binary
RUN pip install djangorestframework

COPY . .

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["bash", "-c"]
CMD ["./docker-entrypoint.sh"]
