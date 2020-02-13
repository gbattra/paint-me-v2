import numpy as np


from tensorflow.keras.preprocessing import image as keras_image_process
from PIL import Image


def load_image(image_path, max_resolution):
    img = Image.open(image_path)
    long = max(img.size)
    scale = max_resolution / long

    img = img.convert('RGB')
    img = img.resize((round(img.size[0] * scale), round(img.size[1] * scale)), Image.ANTIALIAS)
    img = keras_image_process.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    return img


def process_image(image):
    return tf.keras.applications.vgg19.preprocess_input(image)


def unpack_image(image):
    image_copy = image.copy()

    if len(image_copy.shape) == 4:
        image_copy = np.squeeze(image_copy, 0)
    image_copy[:, :, 0] += 103.939
    image_copy[:, :, 1] += 116.779
    image_copy[:, :, 2] += 123.68
    image_copy = image_copy[:, :, ::-1]

    image_copy = np.clip(image_copy, 0, 255).astype('uint8')
    return image_copy
