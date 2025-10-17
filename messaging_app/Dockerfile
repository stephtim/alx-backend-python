<<<<<<< HEAD

FROM python:3.10


WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3.10", "manage.py", "runserver", "0.0.0:8000"]

RUN apt-get update && apt-get install -y \
libpq-dev gcc \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt





EXPOSE 8000
































=======
FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /messaging_app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY Requirements.txt  .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000
EXPOSE 8000

# Default command (overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
>>>>>>> 6e94a15ad0e04ccb334ae164477d76e6f22c87ac
