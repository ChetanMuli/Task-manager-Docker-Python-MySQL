FROM python:3.9-slim

WORKDIR /app

# Install required system dependencies for cryptography & MySQL
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir cryptography PyMySQL

# Copy the rest of the app
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port
EXPOSE 8000

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
