FROM python:3.8.5

RUN mkdir /app

WORKDIR /app
COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8083

CMD python ./app.py