# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any are needed by your python packages)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Install gunicorn, a production-grade WSGI HTTP Server
RUN pip install gunicorn

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 7979

# Run the application using gunicorn
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:7979"]
