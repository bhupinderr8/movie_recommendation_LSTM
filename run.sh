#!/bin/bash

set -e
function cleanup {
  echo "Cleaning up Ports"
  sudo kill `sudo lsof -t -i:8000` &> /dev/null || true
  sudo kill `sudo lsof -t -i:9200` &> /dev/null || true
  sudo kill `sudo lsof -t -i:850` &> /dev/null || true
  sudo -i service elasticsearch stop
}
trap cleanup EXIT

set -o pipefail
sudo kill `sudo lsof -t -i:8000` &> /dev/null || true
sudo kill `sudo lsof -t -i:9200` &> /dev/null || true
sudo kill `sudo lsof -t -i:850` &> /dev/null || true

MODEL_DIR=/home/bhupinder/Documents/movie_recommendation_LSTM/coreapi/dataset/model

sudo -i service elasticsearch start

sudo tensorflow_model_server --rest_api_port=850 --model_name=model --model_base_path="${MODEL_DIR}" >server.log 2>&1 &

python3 manage.py runserver