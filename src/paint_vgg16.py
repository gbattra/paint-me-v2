import tensorflow as tf
import painters.vgg16_painter as vgg16_painter
from PIL import Image

from helpers.image_functions import *


def main():
    content_image = Image.open('./src/images/content/milo.jpg')
    content_image = reshape_and_normalize_image(content_image)

    style_image = Image.open('./src/images/style/colorful_circles.jpg')
    style_image = reshape_and_normalize_image(style_image)

    generated_image = generate_noise_image(content_image)

    model = tf.keras.applications.VGG16()

    painter = vgg16_painter.VGG16_Painter(model)
    painter.paint(content_image, style_image, generated_image)



if __name__ == '__main__':
    main()