FROM python:3.11

WORKDIR /code/

COPY . /code/

COPY requirements.txt /code/

EXPOSE 5672

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
