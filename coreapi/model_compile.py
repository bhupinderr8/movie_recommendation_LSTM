import tensorflow as tf
from keras import backend as K
import shutil
from tensorflow.keras import models
import os


directory_name = os.path.dirname(os.path.abspath("__file__"))

import tensorflow as tf
class CustomLoss(tf.keras.losses.CosineSimilarity):
    def __init__(self):
        super(CustomLoss, self).__init__()
        
    def call(self, y_true, y_pred):
        return super().call(model.layers[0](y_true), model.layers[0](y_pred))

class ReverseEmbedding(tf.keras.layers.Layer):
    def __init__(self):
        super(ReverseEmbedding, self).__init__()
        
    def get_config(self):
        return {}
        
    def call(self, inputs):
        dot_product = tf.matmul(
            tf.nn.l2_normalize(model.layers[0].weights[0], axis=1),
            tf.nn.l2_normalize(inputs, axis=1),
            transpose_b=True)
        return tf.argmax(dot_product,axis=0)

vocab_size=100
vector_size=30
max_val = 209171

model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(max_val, vector_size, mask_zero=True))
model.add(tf.keras.layers.LSTM(128))
model.add(tf.keras.layers.Dense(vector_size, activation='linear'))
model.add(ReverseEmbedding())
loss = CustomLoss()
model.compile(optimizer='adam', loss=loss)
print(model.summary())

file_name = os.path.join(directory_name, 'dataset/keras_model.hdf5')

model.load_weights(file_name)
MODEL_DIR = os.path.join(directory_name, "dataset/model")
version = 1
export_path = os.path.join(MODEL_DIR, str(version))

print('export_path = {}\n'.format(export_path))
if os.path.isdir(export_path):
    print('\nAlready saved a model, cleaning up\n')
    shutil.rmtree(export_path)

tf.keras.models.save_model(
    model,
    export_path,
    overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None
)

