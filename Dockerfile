FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.12-slim
WORKDIR /app
RUN useradd -m bot && chown -R bot:bot /app
USER bot
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
