FROM python:3.12.4-slim

WORKDIR /app

RUN apt update \
    && apt install -y git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -e .

COPY ./ ./

EXPOSE 8080
CMD ["spaces", "serve", "--port", "8080", "--host", "0.0.0.0"]
