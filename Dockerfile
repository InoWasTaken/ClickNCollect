FROM python:3.7-slim-buster

WORKDIR /app
RUN pip3 install flask pymessenger requests flask_cors
COPY api.py main.py db.py /app/

CMD python3 /app/main.py