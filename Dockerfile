# Use Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies including wkhtmltopdf
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the package in development mode
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data reports

# Set environment variables
ENV PYTHONPATH=/app
ENV WKHTMLTOPDF_PATH=/usr/bin/wkhtmltopdf

# Expose the API port
EXPOSE 8080

# Run the API server
CMD ["python", "run_api.py"]
