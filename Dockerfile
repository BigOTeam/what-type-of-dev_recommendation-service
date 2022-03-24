FROM python:3.8.5

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8083

CMD python ./app.py