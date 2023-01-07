import numpy as np


def ElmanNetwork(
        sequence: list,     # Последовательность значений
        windowSize: int,     # Размер окна
        error: float,   # Максимальная ошибка обучения
        maxIter: int,  # Максимальное количество итераций
        secondNeuron: int,     # Максимальное количество нейронов на втором слое
        alpha: float,   # Коэффициент альфа
        predict: int,   # Количество чисел для предсказания
        codeForLearning: str,   # Код для обучения
        codeForTraining: str,   # Код для тренировки
):
    if sequence is None:
        sequence = list(
            map(int, input("Введите последовательность, разделив числа пробелом:\n").split())
        )
    seqLen = len(sequence)
    if windowSize is None:
        windowSize = int(input("Введите размер окна:\n"))
    if windowSize > seqLen:
        raise ("Неверный размер окна, должен быть меньше seqLen")
    if error is None:
        error = int(input("Введите максимальную ошибку обучения:\n"))
    if maxIter is None:
        maxIter = int(input("Введите максимальное количество итераций:\n"))
    if secondNeuron is None:
        secondNeuron = int(input("Введите максимальное количество нейронов на втором слое:\n"))
    if alpha is None:
        alpha = int(input("Введите шаг обучения:\n"))
    if predict is None:
        predict = int(input("Введите количество чисел для предсказания:\n"))
    if codeForLearning is None:
        codeForLearning = input(
            "Введите код обучения:\n"
        )  # on\off for first|on\off for others
    if codeForTraining is None:
        codeForTraining = input(
            "Введите код тренирования:\n"
        )  # on\off for first|on\off for others

    x = []
    y = []
    i = 0
    while i + windowSize < seqLen:
        x.append(sequence[i: i + windowSize])
        y.append(sequence[i + windowSize])
        i += 1
    y = np.array(y)
    x = np.array(x)
    return run(x, y, windowSize, seqLen, error, maxIter, secondNeuron, alpha, predict, codeForLearning, codeForTraining)


def run(
        x: np.array,
        y: np.array,
        windowSize: int,
        seqLen: int,
        error: int,
        maxIter: int,
        secondNeuron: int,
        alpha: float,
        predict: int,
        codeForLearning: str,
        codeForTraining: str,
):
    errorAll = 0
    k = 0
    if codeForLearning[0] == "1":
        context = np.zeros((x.shape[0], secondNeuron))
    else:
        context = np.random.rand(x.shape[0], secondNeuron)
    x = np.concatenate((x, context), axis=1)
    # reshape x matrix to make all samples matrixes (4, 1), not vector (4, )
    x = x.reshape(x.shape[0], 1, x.shape[1])
    w1 = (np.random.rand(windowSize + secondNeuron, secondNeuron) * 2 - 1) / 10
    w2 = (np.random.rand(secondNeuron, 1) * 2 - 1) / 10
    # this code learn for each sample
    for j in range(maxIter):
        errorAll = 0
        if codeForLearning[1] == "1":
            x[:, :, -secondNeuron:] = 0
        for i in range(x.shape[0]):
            hiddenLayer = np.matmul(x[i], w1)
            output = np.matmul(hiddenLayer, w2)
            dy = output - y[i]
            w1 -= alpha * dy * np.matmul(x[i].transpose(), w2.transpose())
            w2 -= alpha * dy * hiddenLayer.transpose()
            try:
                x[i + 1][-secondNeuron:] = hiddenLayer
            except:
                pass
            # print("x=", x[i], "etalon", y[i], "result=", output)
        for i in range(x.shape[0]):
            hiddenLayer = np.matmul(x[i], w1)
            output = np.matmul(hiddenLayer, w2)
            dy = output - y[i]
            errorAll += (dy ** 2)[0]
        print(j + 1, " ", errorAll[0])
        if errorAll <= error:
            break
    k = y[-1].reshape(1)
    X = x[-1, 0, :-secondNeuron]
    out = []
    for i in range(predict):
        X = X[1:]
        train = np.concatenate((X, k))
        X = np.concatenate((X, k))
        train = np.append(train, np.array([0] * secondNeuron))
        if codeForTraining[0]:
            train[-secondNeuron:] = 0
        hidden_layer = np.matmul(train, w1)
        output = np.matmul(hidden_layer, w2)
        k = output
        out.append(k[0])
    return out


if __name__ == "__main__":
    print(
        ElmanNetwork(
            sequence=[1, 2, 6, 24],
            windowSize=3,
            error=0.00000001,
            maxIter=1000000,
            secondNeuron=2,
            alpha=0.0005,
            predict=2,
            codeForLearning="11",
            codeForTraining="11",
        )
    )
