FROM python:3.9

WORKDIR /usr/src/app

COPY . .
COPY requirements.txt .

# RUN pip install -r ./requirements.txt
RUN pip install tensorflow
RUN pip install keras
RUN pip install keras_tuner
RUN pip install matplotlib
RUN pip install numpy
RUN pip install pandas
RUN pip install wandb
RUN pip install flask
RUN pip install werkzeug

EXPOSE 5000

CMD [ "python", "./fashion_item_predict.py" ]