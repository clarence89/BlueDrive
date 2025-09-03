FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install debugpy

COPY . .

EXPOSE 8000 5678

CMD ["sh", "-c", "python -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000"]
