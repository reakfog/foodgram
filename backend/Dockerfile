FROM python:3.8.5

LABEL maintainer="Perchun Evgny V. <evgny_perchun@mail.ru>" 

WORKDIR /code

COPY requirements.txt . 

RUN python -m pip install --upgrade pip 
RUN pip3 install -r requirements.txt 

COPY . .

CMD gunicorn src.wsgi:application --bind 0.0.0.0:8000