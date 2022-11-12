FROM python:3.9

WORKDIR /stroke-prediction-webapp

ADD stroke-prediction-webapp /stroke-prediction-webapp

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "app.py", "--docker"]