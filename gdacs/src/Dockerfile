FROM python:3.8-slim-buster

WORKDIR /usr/app/src

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "./setup.py sdist"]

RUN echo "\n \n \n \n use docker run -it <image name> bash and then python3 client.py --flag (option) \n Option can be one of the following: 1, 2, 3, 4, 5 and clean\n \n \n \n "

