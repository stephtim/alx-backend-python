FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /messaging_app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY Requirements.txt Requirements.txt
RUN pip install -r Requirements.txt
