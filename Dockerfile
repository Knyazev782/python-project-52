FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv

WORKDIR /app

COPY requirements.txt .

RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1 DJANGO_SETTINGS_MODULE=task_manager.settings PORT=8000
RUN python manage.py collectstatic --noinput

CMD gunicorn task_manager.wsgi:application --bind 0.0.0.0:$PORT

