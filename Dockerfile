FROM php:8.3-cli-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /app/api/rate_limit \
    && mkdir -p /app/src/efficiency-calculator/cache \
    && chmod -R a+rwX /app/api/rate_limit \
    && chmod -R a+rwX /app/src/efficiency-calculator/cache

ENV PYTHON_BIN=python3

EXPOSE 8080

CMD ["sh", "-c", "php -S 0.0.0.0:${PORT:-8080} -t api api/index.php"]
