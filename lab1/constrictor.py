import imageio.v2 as imageio

from net import NeuralNetwork
import matplotlib.pyplot as plt
import numpy as np


class Compressor:
    def __init__(self, file_path, wnd_width, wnd_height, p, min_error):
        self.picture = imageio.imread(file_path)
        self.p = p
        self.min_error = min_error
        self.width, self.height, self.channels = self.picture.shape
        self.wnd_width, self.wnd_height = self.check_wnd_size(wnd_width, wnd_height)
        self.image_size = self.wnd_width * self.wnd_height * self.channels

    #   Этот метод нормализует значение каждого канала до [-1, 1]
    def normalize_color(self, window):
        image = np.ravel(window).astype(np.float64)

        for i in range(0, self.image_size):
            image[i] = 2. * image[i] / 255 - 1

        return image    # Входное изображение

    def check_wnd_size(self, wnd_width, wnd_height):
        is_changed = False

        if self.width % wnd_width != 0:
            wnd_width += 1
            is_changed = True

        if self.height % wnd_height != 0:
            wnd_height += 1
            is_changed = True

        if is_changed:
            wnd_width, wnd_height = self.check_wnd_size(wnd_width, wnd_height)

        return wnd_width, wnd_height

    # Строит массив входных изображений
    def prepare_images(self):
        cols = self.width / self.wnd_width
        rows = self.height / self.wnd_height
        inputs = []

        for i in range(0, int(cols)):
            x_pos = i * self.wnd_width
            for j in range(0, int(rows)):
                y_pos = j * self.wnd_height
                inputs.append(self.normalize_color(self.picture[x_pos: x_pos + self.wnd_width,
                                                                y_pos: y_pos + self.wnd_height]))

        return inputs

    def recover_color(self, one_line_image):
        rec_color = np.empty(0, dtype=np.uint8)
        for value in one_line_image:
            cvalue = (value + 1) * 255 / 2
            rec_color = np.append(rec_color, 255 if cvalue > 255 else 0 if cvalue < 0 else cvalue)

        return rec_color

    def recover_window(self, line):
        rec_color = self.recover_color(line)

        out = np.reshape(rec_color, (-1, self.wnd_width, 4))
        return out

    def recover_image(self, rec_images):
        rec_image = np.copy(self.picture)

        cols = self.width / self.wnd_width
        rows = self.height / self.wnd_height
        c = 0

        for i in range(0, int(cols)):
            x_pos = i * self.wnd_width
            for j in range(0, int(rows)):
                y_pos = j * self.wnd_height
                window = self.recover_window(rec_images[c])
                rec_image[x_pos: x_pos + self.wnd_width,
                          y_pos: y_pos + self.wnd_height] = window
                c += 1

        return rec_image

    def process(self):
        print('[ Подготовка входного изображения ]')
        inputs = self.prepare_images()

        print('[ Инициализация сети ]')
        network = NeuralNetwork(inputs, self.p, self.image_size, self.min_error)

        print('[ Начало обучения]')
        network.training()
        # network.load_weights()

        print('[ Начало восстановления изображения ]')
        rec_images = network.process()

        rec_picture = self.recover_image(rec_images)

        print('[ Восстановленное изображение сохранено ]')
        plt.imsave('images/rec_image.png', rec_picture)
