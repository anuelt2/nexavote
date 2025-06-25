# Use official Python slim image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy requirements file first (better caching)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of the project files
COPY . .

# Expose the port Django app runs on
EXPOSE 8000

# Start Gunicorn WSGI server to serve Django app
# Binding to all network interfaces on port 8000
CMD ["gunicorn, config.wsgi:application, --bind, 0.0.0.0:8000"]
