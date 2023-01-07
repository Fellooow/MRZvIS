"""
Сеть Хопфилда с дискретным состоянием, дискретным временем
и синхронным режимимом.
"""

import numpy as np


def func_activation(net: int, f_net: int):
    if net > 0:
        return 1
    elif net < 0:
        return -1
    else:
        return f_net


class Hopfield:
    def __init__(self, size: int):
        self.size = size
        self.weight_matrix = np.zeros((size, size), dtype=int)

    def matrix_weights(self, vector_standards):
        for j in range(self.size):
            for k in range(self.size):
                if j == k:
                    self.weight_matrix[j][k] = 0
                else:
                    self.weight_matrix[j][k] = sum(
                        [vector_standards[l][j] * vector_standards[l][k] for l in range(len(vector_standards))])

    def recognize(self, vector_input):
        vector_y = [0 for _ in range(len(vector_input))]
        while not (np.array_equal(vector_y, vector_input)):
            for k in range(len(vector_input)):
                net = 0
                for j in range(k):
                    net += self.weight_matrix[j][k] * vector_y[j]
                for j in range(k + 1, len(vector_input)):
                    net += self.weight_matrix[j][k] * vector_input[j]
                vector_y[k] = func_activation(net, vector_input[k])
            vector_input = vector_y
        return vector_y


def printing(x):
    for i in range(5):
        s = ''
        if x[i] == -1:
            s += '   '
        else:
            s += ' * '
        if x[i + 5] == -1:
            s += '   '
        else:
            s += ' * '
        if x[i + 10] == -1:
            s += '   '
        else:
            s += ' * '
        print(s)
    print('\n')


if __name__ == '__main__':
    S = [1, 1, 1,
         -1, 1, 1,
         -1, 1, -1,
         1, 1, -1,
         1, 1, 1]

    T = [1, -1, -1,
         -1, -1, 1,
         1, 1, 1,
         1, 1, -1,
         -1, -1, -1]

    U = [1, 1, 1,
         1, 1, -1,
         -1, -1, -1,
         1, 1, 1,
         1, 1, 1]

    SS = [-1, 1, 1,
          -1, 1, 1,
          -1, 1, 1,
          1, -1, -1,
          1, 1, -1]

    TT = [-1, 1, -1,
          -1, -1, 1,
          1, 1, -1,
          1, 1, 1,
          -1, -1, -1]

    UU = [-1, 1, 1,
          1, -1, -1,
          -1, -1, 1,
          1, 1, -1,
          1, 1, 1]

    network = Hopfield(5 * 3)
    network.matrix_weights([S, T, U])
    print(network.weight_matrix)

    printing(S)
    printing(SS)
    printing(network.recognize(SS))

    printing(T)
    printing(TT)
    printing(network.recognize(TT))

    printing(U)
    printing(UU)
    printing(network.recognize(UU))
