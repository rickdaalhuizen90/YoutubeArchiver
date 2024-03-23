FROM python:3.9-alpine

WORKDIR /usr/src/app

COPY src/ .env client_secrets.json ./

RUN apk update && \
    apk add --no-cache \
        build-base \
        python3-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--debug"]
