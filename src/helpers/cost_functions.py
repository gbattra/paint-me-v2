import tensorflow as tf
import numpy as np
import gram_matrix as gm


def compute_content_cost(a_C, a_G):
    m, n_H, n_W, n_C = a_G.get_shape().as_list()

    a_C_unrolled = tf.reshape(tf.transpose(a_C), (n_H * n_W, n_C))
    a_G_unrolled = tf.reshape(tf.transpose(a_G), (n_H * n_W, n_C))

    J_content = (1 / (4 * n_H * n_W * n_C)) * tf.reduce_sum(tf.square(tf.subtract(a_C, a_G)))

    return J_content


def compute_layer_style_cost(a_S, a_G):
    m, n_H, n_W, n_C = a_G.get_shape().as_list()

    a_G = tf.reshape(tf.transpose(a_G), (n_C, n_H * n_W))
    a_S = tf.reshape(tf.transpose(a_S), (n_C, n_H * n_W))

    GS = gm.gram_matrix(a_S)
    GG = gm.gram_matrix(a_G)

    gram_F_norm = tf.reduce_sum(tf.square(tf.subtract(GS, GG)))
    normalizing_const = 4 * np.square(n_C) * np.square(n_H * n_W)

    J_style_layer = gram_F_norm / normalizing_const

    return J_style_layer


def compute_style_cost(model, style_layers):
    J_style = 0

    for layer_name, coeff in style_layers:
        out = model[layer_name]

        a_S = sess.run(out)

        a_G = out

        J_style_layer = compute_layer_style_cost(a_S, a_G)

        J_style += coeff * J_style_layer

    return J_style


def total_cost(J_content, J_style, alpha=10, beta=40):
    J = alpha * J_content + beta * J_style

    return J
