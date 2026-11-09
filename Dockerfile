# Base image: small official Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Document the port the app listens on
EXPOSE 5000

# Command to start the app
CMD ["python", "app.py"]

