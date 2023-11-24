FROM python:3.12.0-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

COPY ./prisma ./prisma

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]
