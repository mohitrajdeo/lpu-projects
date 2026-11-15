FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl bash nodejs && rm -rf /var/lib/apt/lists/*

COPY runner.py /app/runner.py

EXPOSE 9010

CMD ["python3", "/app/runner.py"]

