# import the necessary packages
import os
import random

import cv2 as cv
import keras.backend as K
import numpy as np

from config import img_rows, img_cols, num_classes
from data_generator import get_image, get_category
from data_generator import to_bgr
from model import build_model

if __name__ == '__main__':
    model_weights_path = 'models/model.05-8.3896.hdf5'
    model = build_model()
    model.load_weights(model_weights_path)

    print(model.summary())

    with open('names.txt', 'r') as f:
        names = f.read().splitlines()

    filename = 'valid_ids.txt'
    with open(filename, 'r') as f:
        ids = f.read().splitlines()
        ids = list(map(int, ids))
    samples = random.sample(ids, 10)
    print('samples: ' + str(samples))

    for i in samples:
        name = names[i]
        image = get_image(name)
        category = get_category(i)
        image = cv.resize(image, (img_rows, img_cols), cv.INTER_CUBIC)
        category = cv.resize(category, (img_rows, img_cols), cv.INTER_NEAREST)
        colorful_category = to_bgr(category)
        print('Start processing image: {}'.format(name))

        x_test = np.empty((1, img_rows, img_cols, 3), dtype=np.float32)
        x_test[0, :, :, 0:3] = image / 255.

        out = model.predict(x_test)
        out = np.reshape(out, (img_rows, img_cols, num_classes))
        out = np.argmax(out, axis=2)
        out = to_bgr(out)

        if not os.path.exists('images'):
            os.makedirs('images')

        cv.imwrite('images/{}_image.png'.format(i), image)
        cv.imwrite('images/{}_out.png'.format(i), out)
        cv.imwrite('images/{}_gt.png'.format(i), colorful_category)

    K.clear_session()
