import image_helper
import matplotlib.pyplot as plt
import nst_model as nst
import time
import tensorflow as tf
import nst_trainer


CONTENT_LAYERS = ['block5_conv2']
STYLE_LAYERS = ['block1_conv1',
                'block2_conv1',
                'block3_conv1',
                'block4_conv1',
                'block5_conv1']

STYLE_WEIGHT = 1e-2
CONTENT_WEIGHT = 1e4


if __name__ == '__main__':
    content_image = image_helper.load_img('images/content/content_image.jpg')
    style_image = image_helper.load_img('images/style/style_image_3.jpg')

    # plt.plot()
    # image_helper.image_show(content_image, 'Content Image')

    # plt.plot()
    # image_helper.image_show(style_image, 'Style Image')

    extractor = nst.NSTModel(style_layers=STYLE_LAYERS, content_layers=CONTENT_LAYERS)
    opt = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)
    trainer = nst_trainer.NSTTrainer(extractor,
                                     tf.expand_dims(style_image, 0),
                                     tf.expand_dims(content_image, 0),
                                     opt,
                                     STYLE_WEIGHT,
                                     CONTENT_WEIGHT)
    image = tf.Variable(tf.expand_dims(content_image, 0))  # the image to train / paint
    image = trainer.train(image, epochs=10, steps=100)

    plt.plot()
    image_helper.image_show(image, 'Generated Image')

    image_helper.save_image(image_helper.tensor_to_image(image), 'images/generated/generated_%s.jpg' % time.time())

