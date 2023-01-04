FROM python:3.9

WORKDIR /usr/src/app

COPY . .
COPY requirements.txt .

RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD [ "python", "./fashion_item_predict.py" ]