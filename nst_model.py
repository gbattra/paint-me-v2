import tensorflow as tf
import numpy as np


class NSTModel(tf.keras.models.Model):
    vgg19 = None
    miniVgg = None

    content_layers = []
    style_layers = []

    def __init__(self, style_layers, content_layers):
        super(NSTModel, self).__init__()
        self.style_layers = style_layers
        self.content_layers = content_layers

        self.vgg19 = tf.keras.applications.VGG19(include_top=False, weights='imagenet')

        outputs = [self.vgg19.get_layer(name).output for name in self.style_layers + self.content_layers]
        self.miniVgg = tf.keras.Model([self.vgg19.input], outputs)
        self.miniVgg.trainable = False

    def call(self, inputs):
        inputs = inputs * 255.0
        preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs = self.miniVgg(preprocessed_input)
        style_outputs, content_outputs = (outputs[:len(self.style_layers)],
                                          outputs[len(self.style_layers):])
        gram_style_outputs = [self.gram_matrix(style_output) for style_output in style_outputs]
        style_dict = {
            style_name: value for style_name, value in zip(self.style_layers, gram_style_outputs)
        }
        content_dict = {
            content_name: value for content_name, value in zip(self.content_layers, content_outputs)
        }
        return {
            'content': content_dict,
            'style': style_dict
        }

    def gram_matrix(self, input_tensor):
        result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
        input_shape = tf.shape(input_tensor)
        num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)

        return result / num_locations
