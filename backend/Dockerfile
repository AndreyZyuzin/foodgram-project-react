FROM python:3.10-alpine

WORKDIR /app

RUN pip install gunicorn==20.1.0 

COPY requirements.txt .

RUN pip install --upgrade pip 

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN apk add make
CMD make gunicorn port=${OUT_PORT_FOODGRAM}
