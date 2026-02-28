FROM python:3.12-slim

# Prevent Python from writing .pyc files (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the default Django port
EXPOSE 7979

# Start the server (like run_host.bat)
CMD ["python", "manage.py", "runserver", "0.0.0.0:7979"]
