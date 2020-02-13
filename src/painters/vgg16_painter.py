import numpy as np
import tensorflow as tf
from helpers.image_functions import *

class VGG16_Painter:
    STYLE_LAYERS = [
        ('conv1_1', 0.2),
        ('conv2_1', 0.2),
        ('conv3_1', 0.2),
        ('conv4_1', 0.2),
        ('conv5_1', 0.2)
    ]
    
    def __init__(self, model):
        self.model = model

    
    def paint(self, content_image, style_image, generated_image):
        tf.compat.v1.reset_default_graph()

        sess = tf.compat.v1.InteractiveSession()
        print(content_image.shape)
        # model = self.model(content_image)

    

    
    