import tensorflow as tf


class NSTModel():
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
        
        self.vgg_model = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
        self.vgg_model.trainable = False
        
        self.style_outputs = [self.vgg_model.get_layer(name).output for name in self.style_layers]
        self.content_outputs = [self.vgg_model.get_layer(name).output for name in self.content_layers]

        self.model_outputs = self.style_outputs + self.content_outputs

        self.model = tf.keras.models.Model(self.vgg_model.input, self.model_outputs)


    def _content_loss(self, content, target):
        return tf.reduce_mean(tf.square(content - target))


    def _style_lost(self, style, gram_target):
        gram_style = self._gram_matrix(style)

        return tf.reduce_mean(tf.square(gram_style - gram_target))


    def _total_loss(self, content):
        return tf.reduce_sum(tf.image.total_variation(content))


    def _gram_matrix(self, input_tensor):
        num_channels = int(input_tensor.shape[-1])
        input_vectors = tf.reshape(input_tensor, [-1, num_channels])
        num_vectors = tf.shape(input_vectors)[0]

        gram = tf.matmul(input_vectors, tf.transpose(input_vectors))

        return gram / tf.cast(num_vectors, tf.float32)


    def _feature_representation(self, content_and_style_image):
        content_image = content_and_style_image.processed_content_image
        style_image = content_and_style_image.processed_style_image

        style_outputs = self.model(style_image)
        content_outputs = self.model(content_image)

        style_features = [style_layer[0] for style_layer in style_outputs[:self.num_style_layers]]
        content_features = [content_layer[0] for content_layer in content_outputs[:self.num_content_layers]]

        return style_features, content_features


    def _compute_loss(self, loss_weights, init_image, style_features, content_features):
        style_weight, content_weight, target_weight = loss_weights

        model_outputs = self.model(init_image)

        style_output_features = model.model_outputs[:self.num_style_layers]
        style_content_features = model.model_outputs[self.num_style_layers:]