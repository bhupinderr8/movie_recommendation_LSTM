import numpy as np
import requests
from gensim.models import Word2Vec
import json
import pandas as pd


word_model = Word2Vec.load("coreapi/dataset/word2vec.model")
links = pd.read_csv('coreapi/dataset/links.csv', sep=',', dtype=object)


def word2idx(word):
    # use to generate word from the given index in word model
    return word_model.wv.vocab[word].index


def idx2word(idx):
    # use to generate index from the given word in word model
    return word_model.wv.index2word[idx]


def sample(predictions, temperature=1.0):
    # given output predictions from the tensorflow model, movie id is predicted with max probability
    if temperature <= 0:
        return np.argmax(predictions)
    predictions = np.asarray(predictions).astype('float64')
    predictions = np.log(predictions) / temperature
    exp_preds = np.exp(predictions)
    predictions = exp_preds / np.sum(exp_preds)
    probabilities = np.random.multinomial(1, predictions, 1)
    return np.argmax(probabilities)


def generate_next(text, num_generated=10):
    # given a sequence of movie ids, a next sequence of 10 is generated
    word_idx = [word2idx(word) for word in text.lower().split()]
    for i in range(num_generated):
        data = json.dumps({"instances": [np.array(word_idx).tolist()]})
        headers = {"content-type": "application/json"}
        json_response = requests.post('http://localhost:850/v1/models/model:predict', data=data, headers=headers)
        predictions = json.loads(json_response.text)
        prediction = np.asanyarray(predictions['predictions'])
        idx = sample(prediction[-1], temperature=1)
        word_idx.append(idx)
    return ' '.join(idx2word(idx) for idx in word_idx)


def get_omdb(movie):
    imdb_id = links.loc[links['movieId'] == str(movie)]['imdbId'].tolist()
    json_response = requests.get("http://www.omdbapi.com/?i=tt" + str(imdb_id[0]) + "&apikey=fdfe80e8")
    return json_response


def add_id(json_response, id):
    headers = {"content-type": "application/json"}
    requests.put('http://localhost:9200/movie/_doc/' + id + '?pretty', data=json_response, headers=headers)


def get_movie_descriptions(recommended_movies):
    # convert list of movie ids into a json movie descriptions using elasticsearch api
    movie_dict = recommended_movies.split(' ')
    recommended_movie_titles = []
    for movie in movie_dict:
        response = requests.get(url="http://localhost:9200/movie/_doc/" + str(movie))
        response_dict = json.loads(response.text)
        if response_dict['found']:
            print("Movie Found:", response_dict['_source']['Title'], movie)
            recommended_movie_titles.append(response_dict['_source'])
        else:
            # here omdb rest api is to be used
            json_response = get_omdb(movie)
            movie_description = json.loads(json_response.text)
            recommended_movie_titles.append(movie_description)
            print("Movie Not Found Adding:", movie_description['Title'], "  Id:", movie)
            add_id(json_response, movie)
    return recommended_movie_titles


def generate_list(seq):
    # convert sequence of given movies into recommended movie description and return json format
    movie_ids = get_movie_ids(seq)
    recommended_movie_ids = generate_next(movie_ids)
    print("recommended ids are")
    print(recommended_movie_ids)
    movie_descriptions = get_movie_descriptions(recommended_movie_ids)
    json_response = json.dumps(movie_descriptions)
    return json_response


def get_id(movie_name):
    """{
    "query": {
        "match" : {
            "Title" : "toy story 2"
                }
        }
    }"""

    title_dict = {"Title": movie_name}

    match_dict = {"match": title_dict}

    query_dict = {"query": match_dict}

    data = json.dumps(query_dict)
    headers = {"content-type": "application/json"}

    query_response = requests.get("http://localhost:9200/movie/_search", data=data, headers=headers)
    query_response_dict = json.loads(query_response.text)

    final_id = query_response_dict['hits']['hits'][0]['_id']

    # print(final_id)
    return final_id


def get_movie_ids(movie_list):
    movie_ids = ""
    dict = json.loads(movie_list)
    for i in dict['list']:
        movie_ids = movie_ids + " " + get_id(i)
    return movie_ids
