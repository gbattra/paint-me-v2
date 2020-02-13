import tensorflow as tf


def gram_matrix(self, A):
    GA = tf.matmul(A, tf.transpose(A))

    return GA