import utils.model_loader as model_loader
import utils.image_utils as img_utils


from painters.vgg19_painter import VGG19Painter


MAX_RESOLUTION = 512
NUM_ITERATIONS = 3000


def main():
    content_image = img_utils.load_image('images/content/content_image.jpg', MAX_RESOLUTION)
    style_image = img_utils.load_image('images/style/style_image_2.jpg', MAX_RESOLUTION)

    painter = VGG19Painter()

    painting = painter.paint(content_image, style_image, num_iterations=NUM_ITERATIONS)


if __name__ == '__main__':
    main()