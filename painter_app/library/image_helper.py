import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import PIL.Image
import tensorflow as tf
import os
import time

from google.cloud import storage

mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False


MAX_DIM = 512


def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]

    return PIL.Image.fromarray(tensor)


def load_img(img_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket('sylvan-terra-269023')
    bytes = bucket.blob(img_path).download_as_string()

    img = tf.image.decode_jpeg(bytes, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = MAX_DIM / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)

    return img


def image_show(image, title=None):
    if len(image.shape) > 3:
        image = tf.squeeze(image, axis=0)

    plt.imshow(image)
    if title:
        plt.title(title)

    plt.show()


def clip_0_1(image):
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)


def save_image(image, storage_path):
    # Ensure the pixel-values are between 0 and 255.
    image = np.clip(image, 0.0, 255.0)

    # Convert to bytes.
    image = image.astype(np.uint8)

    # Write the image-file in jpeg-format.
    filename = 'saved_{}.jpg'.format(time.time())
    with open(filename, 'wb') as file:
        PIL.Image.fromarray(image).save(file, 'jpeg')

    storage_client = storage.Client()
    bucket = storage_client.bucket('sylvan-terra-269023')

    filepath = '{}/{}'.format(storage_path, filename)
    blob = bucket.blob(filepath)
    blob.upload_from_filename(filename)

    os.remove(filename)

    return filepath
