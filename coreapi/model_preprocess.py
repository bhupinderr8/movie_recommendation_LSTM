import pandas as pd
import numpy as np
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import keras
from keras.layers import Dense, LSTM
from keras.models import Sequential
import warnings
warnings.filterwarnings('ignore')

dataset = pd.read_csv("coreapi/dataset/ratings.csv", sep=',', nrows=100000)

X_Data = np.asanyarray(dataset.sort_values(['userId', 'timestamp']).groupby('userId')['timestamp'].apply(list))
X_data = dataset.sort_values(['userId', 'timestamp']).groupby('userId')['movieId'].apply(list)
X_data = keras.preprocessing.sequence.pad_sequences(X_data)

l = []
for i in range(1, len(X_data)):
    l1 = []
    for e in X_data[i]:
        l1.append(str(e))
    l.append(l1)

word_model = Word2Vec(l, size=100, min_count=1, window=5, iter=10)
word_model.save('./word2vec.model')
max_sentence_len = len(max(l, key=len))


def word2idx(word):
    return word_model.wv.vocab[word].index


def idx2word(idx):
    return word_model.wv.index2word[idx]


train_x = np.zeros([len(l), max_sentence_len], dtype=np.int32)
train_y = np.zeros([len(l)], dtype=np.int32)
for i, sentence in enumerate(l):
    for t, word in enumerate(sentence[:-1]):
        train_x[i, t] = word2idx(word)
    train_y[i] = word2idx(sentence[-1])

vocab_size = len(word_model.wv.vocab)
embedding_size = 200

model = Sequential()
model.add(keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_size))
model.add(LSTM(units=embedding_size))
model.add(Dense(units=vocab_size))
model.add(keras.layers.Activation('softmax'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

model.summary()
history = model.fit(train_x,train_y, epochs=1)

pd.Series(history.history['loss']).plot(logy=True)
plt.xlabel("Epoch")
plt.ylabel("Train Error")

model.save('coreapi/dataset/keras_model.h5')