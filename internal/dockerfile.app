FROM python:3.12-slim

WORKDIR /app

COPY requirement.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt

COPY . .