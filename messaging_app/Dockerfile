
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
































