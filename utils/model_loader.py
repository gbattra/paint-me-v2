import tensorflow as tf


def load_model():
    try:
        model = tf.saved_model.load('models/vgg19')
        print("model loaded from dir")
    except OSError:
        model = tf.keras.applications.vgg19.VGG19(include_top=False, weights='imagenet')
        tf.saved_model.save(model, 'models/vgg19')
        print("model loaded from cloud and saved to dir")

    return model
