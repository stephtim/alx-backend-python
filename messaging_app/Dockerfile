FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Install System Dependencies and Clean Up
# This block now includes the system libraries for general compilation,
# MySQL, OpenSSL, and the specific dependencies for desktop components (PyGObject, dbus-python).
RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libcurl4-openssl-dev \
    python3-dev \
    # >>> CRITICAL ADDITIONS FOR DESKTOP PACKAGES <<<
    libdbus-1-dev \
    libgirepository1.0-dev && \
    # >>> END CRITICAL ADDITIONS <<<
    rm -rf /var/lib/apt/lists/*

# 2. Copy Requirements and Install Python Packages
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. Copy Application Code
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
