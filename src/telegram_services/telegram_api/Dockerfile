FROM python:3.11

WORKDIR /code/

COPY . /code/

COPY requirements.txt /code/

RUN pip install -r requirements.txt

CMD [ "python", "app/start_polling.py" ]
