FROM python:3.13.2-slim

WORKDIR /app

RUN apt update \
    && apt install -y git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -e .

COPY ./ ./

EXPOSE 8080
CMD ["spaces", "serve", "--port", "8080", "--host", "0.0.0.0"]
