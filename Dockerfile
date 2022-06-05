FROM python:3.10
WORKDIR /reservoirs_bot
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
