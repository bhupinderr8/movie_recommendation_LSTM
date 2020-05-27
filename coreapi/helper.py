import json
import numpy as np
import pandas as pd
import requests
from gensim.models import Word2Vec
import sqlite3

word_model = Word2Vec.load("coreapi/dataset/word2vec.model")
links = pd.read_csv('coreapi/dataset/links.csv', sep=',', dtype=object)


def get_next_recommendation(cur_seq) -> np.array:
    data = json.dumps({"instances": [cur_seq]})
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://localhost:850/v1/models/model:predict', data=data, headers=headers)
    predictions = json.loads(json_response.text)
    prediction = np.asanyarray(predictions['predictions'], dtype=np.float32)
    return prediction[0]


def to_vector(word):
    try:
        return word_model.wv.__getitem__(str(word))
    finally:
        pass


def generate_next(cur_seq, num_generated=20) -> list:
    # given a sequence of movie ids, a next sequence of 10 is generated
    next_seq = [to_vector(movie).tolist() for movie in cur_seq]
    recommend_list = []
    while len(recommend_list) < num_generated:
        candidate_vector = get_next_recommendation(next_seq)
        next_id = word_model.wv.most_similar(positive=[candidate_vector], topn=1)
        recommend_list.append(next_id[0][0])
        next_seq.append(candidate_vector.tolist())
    return recommend_list


def id_to_imdb(movie_id) -> str:
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("select imdbid_id from coreapi_link where movieid=?", [movie_id])
        imdb_id = cursor.fetchone()[0]
        cursor.close()
    return imdb_id


def imdb_to_id(imdb_id) -> int:
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("select movieid from coreapi_link where imdbid_id = ?", [imdb_id])
        movie_id = int(cursor.fetchone()[0])
        cursor.close()
    return movie_id


def generate_list(seq) -> list:
    # convert sequence of given movies into recommended movie description and return json format
    if seq:
        movie_ids = list(map(imdb_to_id, seq))
    else:
        # perform random selection to get recommendations
        return ["tt0000001"]
    recommended_movie_ids = generate_next(movie_ids)
    recommended_movie_ids = map(id_to_imdb, recommended_movie_ids)
    return list(recommended_movie_ids)


if __name__ == "__main__":
    print(generate_list(["tt0114952"]))
