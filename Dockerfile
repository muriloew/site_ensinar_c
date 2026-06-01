FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=10000
CMD gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:$PORT
