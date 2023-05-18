FROM python:3.11.3-bullseye

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get install poppler-utils -y

RUN apt install -y tesseract-ocr

COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./
