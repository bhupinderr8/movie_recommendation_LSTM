import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_recommendation_LSTM.settings")
from coreapi import models

directory_name = os.pardir
filename = os.path.join(directory_name, 'coreapi/dataset/imdb/name_basics.tsv')
print(filename)

with open(filename) as f:
    reader = csv.reader(f, delimiter="\t")
    for i in next(reader):
        print (i)
