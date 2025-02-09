FROM python:3.12-alpine 
RUN apk update  && apk upgrade \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo \
    && apk add tesseract-ocr tesseract-ocr-data-hin tesseract-ocr-data-eng ghostscript\
    && rm -rf /var/cache/apk/*
WORKDIR /app/
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir --upgrade --requirement /app/requirements.txt
RUN apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo
COPY . .
CMD ["python" ,"main.py"]