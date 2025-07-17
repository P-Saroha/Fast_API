# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Copy and install dependencies
COPY model_improvement/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your full FastAPI app folder
COPY model_improvement /app/model_improvement

# Move into the correct working directory for uvicorn
WORKDIR /app/model_improvement

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

