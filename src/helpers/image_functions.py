import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

class CONFIG:
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 300
    COLOR_CHANNELS = 3
    NOISE_RATIO = 0.6


def generate_noise_image(content_image, noise_ratio=CONFIG.NOISE_RATIO):
    noise_image = np.random.uniform(-20, 20, (1, CONFIG.IMAGE_HEIGHT, CONFIG.IMAGE_WIDTH, CONFIG.COLOR_CHANNELS)).astype('float32')
    
    input_image = noise_image * noise_ratio + content_image * (1 - noise_ratio)
    
    return input_image


def reshape_and_normalize_image(image):
    
    resized_image = image.resize((CONFIG.IMAGE_WIDTH, CONFIG.IMAGE_HEIGHT), Image.ANTIALIAS)
    normalized_image = np.asarray(resized_image) / 255

    return normalized_image