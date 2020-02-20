PAINTER_CONFIGS = [
    {
        'STYLE_IMAGE_PATH': 'https://i.imgur.com/TltddGV.jpg',
        'CONTENT_LAYERS': ['block5_conv2'],
        'STYLE_LAYERS': ['block1_conv1',
                        'block2_conv1',
                        'block3_conv1',
                        'block4_conv1',
                        'block5_conv1'],
        'STYLE_WEIGHT': 1e-2,
        'CONTENT_WEIGHT': 1e3,
    }
]