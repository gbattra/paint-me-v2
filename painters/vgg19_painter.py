import tensorflow as tf

from tensorflow.keras import models


class VGG19Painter():
    def __init__(self):
        self.content_layers = ['block5_conv2']
        self.style_layers = [
            'block1_conv1',
            'block2_conv1',
            'block3_conv1',
            'block4_conv1',
            'block5_conv1'
        ]

        self.num_content_layers = len(self.content_layers)
        self.num_style_layers = len(self.style_layers)

        self.vgg_model = tf.keras.applications.vgg19.VGG19(include_top=False, weights='imagenet')
        self.vgg_model.trainable = False

        self.style_outputs = [self.vgg_model.get_layer(name).output for name in self.style_layers]
        self.content_outputs = [self.vgg_model.get_layer(name).output for name in self.content_layers]

        self.model_outputs = self.style_outputs + self.content_outputs

        self.model = models.Model(self.vgg_model.input, self.model_outputs)


    def paint(self,
        content_image,
        style_image,
        num_iterations=3000,
        content_weight=1e-1,
        style_weight=1e2,
        target_weight=1,
        save=False):

        for layer in self.model.layers:
            layer.trainable = False

        content_features, style_featuers = self._get_features(content_image, style_image)


    def _get_features(self, content_image, style_image):
        content_outputs = self.model(content_image)
        style_outputs = self.model(style_image)

        style_features = [style_layer[0] for style_layer in style_outputs[:self.num_style_layers]]
        content_features = [content_layer[0] for content_layer in content_outputs[self.num_style_layers:]]

        return content_features, style_features