# Dockerfile for Skylus Analytics Platform
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs exports cache config backups reports templates

# Create non-root user for security
RUN useradd -m -s /bin/bash skylus && \
    chown -R skylus:skylus /app

# Switch to non-root user
USER skylus

# Expose port
EXPOSE 9501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:9501/_stcore/health || exit 1

# Set environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=9501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run the application
CMD ["streamlit", "run", "main.py", "--server.port=9501", "--server.address=0.0.0.0", "--server.headless=true"]