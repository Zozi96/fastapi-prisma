#!/bin/sh

if [ "$DEBUG" = "False" ]; then
  cd /app/prisma && prisma migrate deploy
  cd /app
fi

python src/main.py