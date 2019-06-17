import keras
import tensorflow as tf
from keras import backend as K
import shutil
from keras.models import load_model
import os

K.set_learning_phase(0)


dirname = os.path.dirname(os.path.abspath("__file__"))
model = load_model(os.path.join(dirname, 'dataset/keras_model.h5'))
print(model.outputs)


MODEL_DIR = os.path.join(dirname, "dataset/model")
version = 1
export_path = os.path.join(MODEL_DIR, str(version))
print('export_path = {}\n'.format(export_path))
if os.path.isdir(export_path):
    print('\nAlready saved a model, cleaning up\n')
    shutil.rmtree(export_path)

tf.saved_model.simple_save(
    keras.backend.get_session(),
    export_path,
    inputs={'inpput_img': model.input},
    outputs={'output': model.output})