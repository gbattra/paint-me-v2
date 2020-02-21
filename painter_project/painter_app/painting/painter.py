import tensorflow as tf

from . import image_helper
from . import nst_trainer
from . import nst_model as nst_model


class Painter(object):
    def __init__(self, pretrained_model, content_layers, style_layers, content_weight, style_weight):
        self.pretrained_model = pretrained_model
        self.content_layers = content_layers
        self.style_layers = style_layers

        self.content_weight = content_weight
        self.style_weight = style_weight

    def paint(self, content_image_path, style_image_path):
        content_path = tf.keras.utils.get_file('content_image.jpg', content_image_path)
        style_path = tf.keras.utils.get_file('style_image.jpg', style_image_path)
        content_image = image_helper.load_img(content_path)
        style_image = image_helper.load_img(style_path)

        # plt.plot()
        # image_helper.image_show(content_image, 'Content Image')

        # plt.plot()
        # image_helper.image_show(style_image, 'Style Image')

        extractor = nst_model.NSTModel(
            pretrained_model=self.pretrained_model,
            style_layers=self.style_layers,
            content_layers=self.content_layers)
        opt = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)
        trainer = nst_trainer.NSTTrainer(extractor,
                                         tf.expand_dims(style_image, 0),
                                         tf.expand_dims(content_image, 0),
                                         opt,
                                         self.style_weight,
                                         self.content_weight)
        image = tf.Variable(tf.expand_dims(content_image, 0))  # the image to train / paint
        image = trainer.train(image, epochs=10, steps=1)

        # plt.plot()
        # image_helper.image_show(image, 'Generated Image')

        # image_helper.save_image(image_helper.tensor_to_image(image), 'generated_%s.jpg' % time.time())

        return image_helper.tensor_to_image(image)
