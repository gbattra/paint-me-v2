import tensorflow as tf
import image_helper


class NSTTrainer(object):
    def __init__(self,
                 model,
                 style_image,
                 content_image,
                 optimizer,
                 style_weight,
                 content_weight):
        self.model = model

        self.target_styles = self.model(style_image)['style']
        self.target_contents = self.model(content_image)['content']

        self.optimizer = optimizer
        self.style_weight = style_weight
        self.content_weight = content_weight

    @tf.function
    def train_step(self, image):
        with tf.GradientTape() as tape:
            outputs = self.model(image)
            loss = self.style_content_loss(
                outputs['style'],
                outputs['content'],
                self.target_styles,
                self.target_contents
            )

        grad = tape.gradient(loss, image)
        self.optimizer.apply_gradients([(grad, image)])
        image.assign(image_helper.clip_0_1(image))

    def style_content_loss(self,
                           generated_styles,
                           generated_contents,
                           target_styles,
                           target_contents):
        style_loss = tf.add_n([tf.reduce_mean((generated_styles[name] - target_styles[name]) ** 2)
                               for name in generated_styles.keys()]) * (self.style_weight / len(generated_styles))
        content_loss = tf.add_n([tf.reduce_mean((generated_contents[name] - target_contents[name]) ** 2)
                                 for name in generated_contents.keys()]) * (self.content_weight / len(generated_contents))

        return style_loss + content_loss

