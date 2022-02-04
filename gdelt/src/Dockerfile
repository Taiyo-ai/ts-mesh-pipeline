FROM python:3.8-slim-buster

WORKDIR /home/gdelt

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3"]
