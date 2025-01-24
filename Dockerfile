FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM gcr.io/distroless/python3:latest

WORKDIR /app

COPY --from=builder /app/ /app/
COPY --from=builder /root/.local/ /home/nonroot/.local/
ENV PATH="/home/nonroot/.local/bin:$PATH"

USER nonroot

EXPOSE 8000

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
