FROM python:3.12-slim

WORKDIR /usr/src/app

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    automake \
    gcc \
    g++ \
    subversion \
    python3-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

RUN mkdir -p received

COPY . /usr/src/app
COPY requirement.txt /usr/src/app/requirement.txt

RUN pip install -r requirement.txt