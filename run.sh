#!/bin/bash

MODEL_DIR=/home/bhupinder/PycharmProjects/movie_recommendation_LSTM/coreapi/dataset

sudo nohup tensorflow_model_server --rest_api_port=850 --model_name=model --model_base_path="${MODEL_DIR}" >server.log 2>&1 &

nohup /home/bhupinder/elasticsearch-6.5.4/bin/elasticsearch  >server_elastic.log 2>&1 &

python3 manage.py runserver