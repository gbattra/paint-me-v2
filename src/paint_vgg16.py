import painters.vgg16_painter as vgg16_painter
from helpers.image_functions import *


def main():
    content_filename = './src/images/content/milo.jpg'
    content_image = load_image(content_filename)

    style_filename = './src/images/style/colorful_circles.jpg'
    style_image = load_image(style_filename)

    painter = vgg16_painter.VGG16_Painter()
    painter.paint(content_image, style_image)



if __name__ == '__main__':
    main()