# Use official Python slim image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (better caching)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of the project files
COPY . .

# Copy and set entrypoint script
# COPY entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh

# Expose the port Django app runs on
EXPOSE 8000

# Entrypoint to run migrations, collectstatic, and start Gunicorn
# ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn, config.wsgi:application, --bind, 0.0.0.0:8000"]
