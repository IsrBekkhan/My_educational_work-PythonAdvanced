FROM python:3.10

RUN apt-get update && apt-get install -y python3-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY src /app/src/

WORKDIR /app/src

ENV HOST=0.0.0.0 PORT=5000

CMD gunicorn --bind=${HOST}:${PORT} --workers=2 main_app:app