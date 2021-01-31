import json
import requests
import sqlite3


def get_next_recommendation(cur_seq) -> int:
    data = json.dumps({"instances": [cur_seq]})
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://localhost:850/v1/models/model:predict', data=data, headers=headers)
    prediction = json.loads(json_response.text)['predictions']
    return prediction


def generate_next(cur_seq, num_generated=20) -> list:
    # given a sequence of movie ids, a next sequence of 10 is generated
    recommend_list = []
    while len(recommend_list) < num_generated:
        candidate = get_next_recommendation(cur_seq)
        recommend_list.extend(candidate)
        cur_seq.extend(candidate)
    return recommend_list


def id_to_imdb(movie_id) -> str:
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("select imdbid_id from coreapi_link where movieid=?", [movie_id])
        try:
            imdb_id = cursor.fetchone()[0]
        except:
            imdb_id = None
        cursor.close()
    return imdb_id


def imdb_to_id(imdb_id) -> int:
    with sqlite3.connect("db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute("select movieid from coreapi_link where imdbid_id = ?", [imdb_id])
        try:
            movie_id = int(cursor.fetchone()[0])
        except:
            movie_id = None
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
