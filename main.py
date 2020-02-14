import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


from image_functions import *
from PIL import Image
from io import BytesIO


CONTENT_LAYERS = ['block4_conv2']
STYLE_LAYERS = [
    'block1_conv1',
    'block2_conv1',
    'block3_conv1',
    'block4_conv1',
    'block5_conv1'
]


def create_model():
    model = tf.keras.applications.vgg19.VGG19(include_top=False, weights='imagenet')
    model.trainable = False
    output_layers = [model.get_layer(layer).output for layer in (CONTENT_LAYERS + STYLE_LAYERS)]

    return tf.keras.models.Model(model.input, output_layers)


def get_content_loss(generated_image, content_image):
    return tf.reduce_mean(tf.square(generated_image, content_image))


def gram_matrix(output):
    channels = output.shape[-1]
    a = tf.reshape(output, [-1, channels])
    gram_matrix = tf.matmul(a, a, transpose_a=True)
    n = int(gram_matrix.shape[0])

    return gram_matrix / tf.cast(n, 'float32'), n


def get_style_loss(generated_style_image, base_style_image):
    generated_style_gram, generated_style_gram_height = gram_matrix(generated_style_image)
    base_style_gram, base_style_gram_height = gram_matrix(base_style_image)

    assert generated_style_gram_height == base_style_gram_height

    gram_features = int(generated_style_gram.shape[0])
    loss = tf.reduce_mean(tf.square(generated_style_gram - base_style_gram) / (2 * int(generated_style_gram_height) * (gram_features)) ** 2)

    return loss


def get_total_loss(generated_output, base_content_output, base_style_output, alpha=0.99, beta=0.01):
    generated_image_styles = generated_output[len(CONTENT_LAYERS):]
    base_image_styles = base_style_output[len(CONTENT_LAYERS):]

    generated_image_content = generated_output[:len(CONTENT_LAYERS)]
    base_image_content = base_content_output[:len(CONTENT_LAYERS)]

    style_loss = 0
    for i in range(len(generated_image_styles)):
        style_loss += get_style_loss(generated_image_styles[i], base_image_styles[i])

    content_loss = 0
    for i in range(len(generated_image_content)):
        content_loss += get_content_loss(generated_image_content[i], base_image_content[i])

    return alpha * content_loss + beta * style_loss


def generate_image(
    model,
    optimizer,
    content_image,
    style_image,
    iterations=1000,
    content_weight=1.0,
    style_weight=10.0):

    content_image = tf.keras.applications.vgg19.preprocess_input(np.expand_dims(content_image, axis=0))
    style_image = tf.keras.applications.vgg19.preprocess_input(np.expand_dims(style_image, axis=0))

    generated_image = tf.Variable(style_image + tf.random.normal(style_image.shape))

    content_output = model(content_image)
    style_output = model(style_image)

    best_loss = float('inf')
    best_image = generated_image.numpy()
    losses = []
    images = []
    for i in range(iterations):
        with tf.GradientTape() as tape:
            print('Iteration: {0}'.format(i))
            tape.watch(generated_image)
            generated_output = model(generated_image)
            loss = get_total_loss(generated_output, content_output, style_output)
            losses.append(loss)

            gradients = tape.gradient(loss, generated_image)

            optimizer.apply_gradients(list(zip([gradients], [generated_image])))

            generated_image_clipped = tf.clip_by_value(generated_image, 0, 255)
            generated_image.assign(generated_image_clipped)

            if i % 10 == 0:
                images.append(generated_image.numpy())

            if loss < best_loss:
                best_image = generated_image.numpy()
                best_loss = loss

    return best_image, images, losses


if __name__ == '__main__':
    content_image = load_image('images/content/content_image.jpg')
    style_image = load_image('images/style/style_image_2.jpg')

    model = create_model()
    optimizer = tf.optimizers.Adam(learning_rate=5)
    
    painted_image = generate_image(
        model,
        optimizer,
        content_image,
        style_image
    )
