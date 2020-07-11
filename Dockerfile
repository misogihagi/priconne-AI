FROM python:latest

#COPY pri.traineddata /usr/share/tesseract-ocr/4.00/

WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get -y install \
    tesseract-ocr 
RUN apt-get clean

		
RUN pip install --upgrade pip; \
    pip install pip \
    pytesseract \
    pillow \
    requests \
    redis \
    twython \
    flask


CMD python main.py
