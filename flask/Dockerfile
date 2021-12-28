FROM python:3.9

WORKDIR /app

COPY . /app

EXPOSE 8000:8000

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt


CMD [ "python", "app.py" ]



