# Use the official Python base image with a minimal footprint
FROM python:3.11-slim

# Set environment variables for Python to behave predictably in Docker
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures that Python outputs are logged immediately to the console
ENV PYTHONUNBUFFERED 1

# Create and set the working directory for the application
WORKDIR /app

# Install system dependencies required for building Python packages (if needed)
# and clean up apt cache afterwards to keep the image small
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker cache
# This means docker won't reinstall packages if requirements.txt hasn't changed
COPY requirements.txt .

# Install Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Specify the command to run the application using Uvicorn
# --host 0.0.0.0 allows connections from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
