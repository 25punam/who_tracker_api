FROM python:3.13.3-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl + psql client
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# uv copy (fast pip alternative)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# requirements file (root me)
COPY requirements.txt .

RUN uv pip install -r requirements.txt --system

# project code (root)
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
