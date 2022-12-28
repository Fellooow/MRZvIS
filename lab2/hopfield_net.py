"""
Сеть Хопфилда с дискретным состоянием, дискретным временем
и синхронным режимимом.
Использована функция знака в качестве функции активации
"""

import numpy as np


class Network:
    def __init__(self, reference, test, view="full"):  # Функция инициализации экземляра объекта класса

        self.printOption = view  # Инициализация переменной view для настройки вывода результатов в консоль
        self.setPrintOtions()  # Вызов функции для настройки вывода результатов в консоль

        # Логика
        self.xVectors = []  # Инициализация массива хранящего векторы "x" (эталонные образы)
        self.xTMultiplyX = []  # Инициализация массива хранящего значения произведения матр. "X" трансп. на матр. "X"
        self.weights = []  # Инициализация массива хранящего матрицу "W" (матрицу весовых коэффициентов)
        self.zeroedWeights = []  # Инициализация массива хранящего занулённую матрицу "W" (матрицу весовых коэффициентов)
        self.yVector = []  # Инициализация массива хранящего вектор "y" (тестовый образ)
        self.weightsMultiplyY = []  # Инициализация массива хранящего произведение занулённой матрицы "W" на вектор "y"
        self.signWeightsMultiplyY = []  # Ин. мас. храниящего значения ф-и "sign" от пр. зан. матр. "W" на век. "y"
        self.recognizedImage = 0  # Инициализация номера распознанного образа

        self.create_x_vectors(reference)  # Вызов функции обработки векторов "x"
        self.calculate_xT_multiply_x()  # Вызов функции умножения матр. "x" трансп. на матр. "x"
        self.calculate_weights()  # Вызов функции расчёта матрицы "W"
        self.zero_out_x()  # Вызов функции зануления матрицы "W"
        self.create_y_vector(test)  # Вызов функции обработки вектора "y"
        self.calculate_zeroed_weights_multiply_y()  # Вызов функции вычисления произв. занулённой матрицы "W" на вектор "y"
        self.recognize()  # Вызов функции определения номера распознанного образа

    # Функции отвечающие за настройку вывода
    def setPrintOtions(self):  # Функция для настройки вывода результатов в консоль
        if self.printOption == "full":  # Если переменная "printOption" равна "full"
            np.set_printoptions(threshold=np.inf)  # Выводить в консоль большие матрицы полностю

    # Функции отвечающие за алгоритм
    def create_x_vectors(self, vectors):  # Функция обработки векторов "x"
        for vector in vectors:  # Для каждого вектора переданного в экземпляр
            numpy_array = np.array(vector)  # Преобразовать вектор в массив numpy
            self.xVectors.append(numpy_array)  # Добавить массив numpy в массив хранящий массивы "x"

    def calculate_xT_multiply_x(self):  # Функция умножения матр. X трансп. на матр. X
        for numpy_array in self.xVectors:  # Для каждого вектора в массиве векторов "x"
            xT = numpy_array.reshape(numpy_array.size, 1)  # Создание транспонированной матрицы "xt" из вектора "x"
            xTMultiplyX = xT * numpy_array  # Умножение матрицы "xt" на матрицу "x"
            self.xTMultiplyX.append(xTMultiplyX)  # Добавление результата в массив

    def calculate_weights(self):  # Функция расчёта матрицы W
        weights = 0  # Создание временной переменной для суммирования матриц
        for matrix in self.xTMultiplyX:  # Для каждой матрицы из массива матриц "xt * t"
            weights = weights + matrix  # Сумма матриц равна результату сложения существующей матрицы "W" и текущей матрицы "matrix"
        self.weights = weights  # Присвоение перменной w значения суммы матриц

    def zero_out_x(self):  # Функция зануления матрицы W
        self.zeroedWeights = self.weights * (  # Матрица W поэлементно умножается на единичную матрицу, где на гл. диагонали нули
                np.ones(self.xVectors[0].size, int) - np.identity(self.xVectors[0].size, int)
        )

    def create_y_vector(self, vector):  # Функции обработки вектора "y"
        numpy_array = np.array(vector)  # Преобразование ветора "y" в массив "numpy"
        self.yVector.append(numpy_array)  # Добавить массив numpy в массив храниящий массивы "y"

    def calculate_zeroed_weights_multiply_y(self):  # Функция вычисления произведения занулённой матрицы "W" на вектор "y"
        for numpy_array in self.yVector:  # Для каждого вектора "y" (тестовго образа)
            y = numpy_array.reshape(numpy_array.size, 1)  # Формируем матрицу размера (n, 1) из вектора размера (n)
            zeroedWeightsMultiplyY = np.matmul(self.zeroedWeights, y)  # Умножаем матрицу "W" на матрицу "y"
            self.weightsMultiplyY.append(zeroedWeightsMultiplyY)  # Добавляем результат умножения в массив
            signZeroedWeightsMultiplyY = np.sign(zeroedWeightsMultiplyY)  # Находим "sign" для эл. в полученной матрице
            self.signWeightsMultiplyY.append(signZeroedWeightsMultiplyY)  # Добавляем результат вычислений sign в массив
            temporary_variable = np.zeros(1)  # Инициализируем временную переменную для сравнения матриц

            while True:  # Бесконечный цикл
                zeroedWeightsMultiplyY = np.matmul(self.zeroedWeights, signZeroedWeightsMultiplyY)  # Умножаем W на sign(y)
                signZeroedWeightsMultiplyY = np.sign(zeroedWeightsMultiplyY)  # Обновляем матрицу tanh(y)

                # Функция сравнения состояния матрицы в момент "t" и "t-1"
                requirement = (  # Если первые четыре символа после запятой совпадают
                        np.around(temporary_variable, 4) == np.around(signZeroedWeightsMultiplyY, 4)
                )  # то считатеся, что сеть достигла релаксации
                counter = 0
                for element in requirement:
                    if element == [False]:
                        counter = counter + 1

                if counter == 0:  # Если матрица sign(y) на шаге n совпадает с n - 1
                    break  # Завершить цикл

                temporary_variable = signZeroedWeightsMultiplyY  # Обновить временную переменную
                self.weightsMultiplyY.append(zeroedWeightsMultiplyY)  # Добавить матрицу W в список
                self.signWeightsMultiplyY.append(signZeroedWeightsMultiplyY)  # Добавить sign(y) в список

    def recognize(self):  # Функция определения найденного образа
        recognizedImage = np.sign(self.signWeightsMultiplyY[-1])  # Инициализация распознанного обрааза
        recognizedImage = recognizedImage.reshape(1, recognizedImage.size)[0]  # Подготовка вектора
        recognizedImage = recognizedImage.astype(int)  # Подготовка вектора
        count = 1  # Инициализация вспомогательной переменной

        for numpy_array in self.xVectors:  # Для кажого вектора "x"
            numpy_array = np.sign(numpy_array)  # Подготовка вектора "x"
            numpy_array = np.around(numpy_array, 1)  # Подготовка вектора "x"
            numpy_array = numpy_array.astype(int)  # Подготовка вектора "x"

            temporary_counter_1 = 0  # Инициализация вспомогательной переменной
            temporary_counter_2 = 0  # Инициализация вспомогательной переменной
            negative_numpy_array = numpy_array * -1

            for i in range(recognizedImage.size):  # Для каждого элемента в распознанном образе
                # Если все элементы расп. обр. и вектора "x" № "i" равны
                if recognizedImage[i] == numpy_array[i]:
                    temporary_counter_1 = temporary_counter_1 + 1  # Увелисть времнную переменную на 1
                    if temporary_counter_1 == recognizedImage.size:  # Если все элементы равны
                        self.recognizedImage = count  # Вернуть переменную
                        break  # Прекратить поиск

                # Если все элементы расп. обр. и вектора "x" № "i" умноженного на (-1) равны
                if recognizedImage[i] == negative_numpy_array[i]:
                    temporary_counter_2 = temporary_counter_2 + 1  # Увелисть времнную переменную на 1
                    if temporary_counter_2 == recognizedImage.size:  # Если все элементы равны
                        self.recognizedImage = - count  # Вернуть переменную
                        break  # Прекратить поиск

            count = count + 1

    # Функции отвечающие за вывод данных в консоль

    def print_x_vectors(self):  # Вывести в консоль векторы "x"
        for numpy_array in self.xVectors:  # Для каждого массива numpy в массиве содержащем векторы "x"
            print(numpy_array)  # Вывести в консоль массив numpy

    def print_xT_multiply_x(self):  # Вывести в консоль значения произведения матрицы "xt" и "x"
        for numpy_array in self.xTMultiplyX:  # Для каждого массива numpy в массиве содержащем произведения "xt" и "x"
            print(numpy_array)  # Вывести в консоль массив numpy

    def print_w(self):  # Вывести в консоль матрицу "W"
        print(self.weights)  # Вывести в консоль матрицу "W"

    def print_zeroed_weights(self):  # Вывести в консоль занулённую матрицу "W"
        print(self.zeroedWeights)  # Вывести в консоль занулённую матрицу "W"

    def print_y_vector(self):  # Вывести в консоль вектор "y"
        print(self.yVector[0])  # Вывести в консоль вектор "y"

    def print_w_multiply_y(self):  # Вывести в консоль значения произведений матрицы "W" на вектор "y"
        for numpy_array in self.weightsMultiplyY:  # Для каждого массива numpy в массиве содержащем результаты "W * y"
            print(numpy_array)  # Вывести в консоль массив numpy

    def print_sign_w_multiply_y(self):  # Вывести в консоль значения произведений занулённой матрицы "W" на вектор "y"
        for numpy_array in self.signWeightsMultiplyY:  # Для каждого массива numpy в массиве содержащем "sign(W * y)"
            print(numpy_array)  # Вывести в консоль массив numpy

    def print_result(self):  # Вывести в консоль результат
        print(f"Итераций выполнено: {len(self.signWeightsMultiplyY) + 1}")  # Итерации понадобившиеся для релаксации сети
        print(f"Последняя итерация sign(W * y): ")
        for element in self.signWeightsMultiplyY[-1]:  # Последний результат "sign(W * y)"
            print(" ", element)
        if self.recognizedImage > 0:
            print(f"Тестовый образ распознан как образ №{self.recognizedImage}")
        else:
            print(f"Тестовый образ распознан как негатив образа №{self.recognizedImage * -1}")


def main():  # Основная функция
    start = Network(
        # Эталонные образы
        reference=[[
            -0.5, 0.5, -0.5,  # Символ "A"
            0.5, 0.5, 0.5,
            0.5, -0.5, 0.5
        ], [
            0.5, 0.5, 0.5,  # Символ "C"
            0.5, -0.5, -0.5,
            0.5, 0.5, 0.5,
        ], [
            0.5, 0.5, -0.5,  # Символ "D"
            0.5, -0.5, 0.5,
            0.5, 0.5, -0.5
        ], [
            -0.5, -0.5, 0.5,    # Символ "1"
            -0.5, 0.5, 0.5,
            -0.5, -0.5, 0.5,
        ], [
            0.5, 0.5, 0.5,    # Символ "0"
            0.5, -0.5, 0.5,
            0.5, 0.5, 0.5,
        ], [
            -0.5, 0.5, 0.5,    # Символ "7"
            -0.5, 0.5, 0.5,
            -0.5, -0.5, 0.5,
        ]],
        # Образ для проверки
        test=[  # Зашумленный символ "C"
            0.9, 0.9, 0.9,
            0.2, 0.2, -0.2,
            0.2, 0.8, -0.8
        ]
    )

    start.print_result()


if __name__ == "__main__":  # Если файл называется main.py
    main()  # Вызов главной функции
