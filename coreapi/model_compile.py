import tensorflow as tf
from keras import backend as K
import shutil
from tensorflow.keras import models
import os


sess = tf.compat.v1.InteractiveSession()
K.set_learning_phase(0)
directory_name = os.path.dirname(os.path.abspath("__file__"))
model = models.load_model(os.path.join(directory_name, 'dataset/keras_model.h5'))

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

