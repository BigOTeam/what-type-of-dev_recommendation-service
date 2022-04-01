FROM tensorflow/tensorflow:2.8.0

RUN mkdir /app

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8083

CMD python ./app.py