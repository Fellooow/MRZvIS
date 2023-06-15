#########################################################################
# Лабораторная работа #2 по дисциплине ЛОИС                             #
# Выполнена студентом группы 021703 БГУИР Колосовским Егором Сергеевичем#
# Файл содержит функции проверки нейтральности заданной формулы         #
# 2023.03.21 v0.0.1                                                     #
#########################################################################
from functools import reduce
from GetNumberOfSubformulas import FormulaChecker

GRAMMAR = {
    'symbol': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
               'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
    'const': ['1','0'],
    'bracket': ['(',')'],
    'unar_operation': ['!'],
    'bin_operation': ['/\\','\/','->','~']
}

MAX_ELEM_LENGTH = 2

TRUTH_TABLE_BINARY = {
    '&': [
        ['0', '0', '0'],
        ['0', '1', '0'],
        ['1', '0', '0'],
        ['1', '1', '1'],
    ],
    '|': [
        ['0', '0', '0'],
        ['0', '1', '1'],
        ['1', '0', '1'],
        ['1', '1', '1'],
    ],
    '->': [
        ['0', '0', '1'],
        ['0', '1', '1'],
        ['1', '0', '0'],
        ['1', '1', '1'],
    ],
    '~': [
        ['0', '0', '1'],
        ['0', '1', '0'],
        ['1', '0', '0'],
        ['1', '1', '1'],
    ]
}

TRUTH_TABLE_UNARY = {
    '!': [
        ['0', '1'],
        ['1', '0'],
    ]
}

operandArr = []
operatorArr = []
resultArr = []
table = []
check = FormulaChecker()

def size(obj):
    size = 0
    for key in obj:
        if key in obj:
            size += 1
    return size


def check_is_neutral(value):

    if not check.is_formula(value):
        print('Invalid formula')
        return False
    arr = calculating()
    if reduce(lambda product, value: product * value, arr) == 1 or reduce(lambda product, value: product + value, arr) == 0:
        print("This formula isn't neutral")
        return False
    else:
        print('This formula is neutral')
        return True

def find_operand_arr():
    _operandArr = operandArr.copy()

    for i in range(len(_operandArr)):
        if GRAMMAR['const'].index(_operandArr[i]) >= 0:
            _operandArr.pop(i)
            i -= 1
        else:
            for j in range(i):
                if _operandArr[j] == _operandArr[i]:
                    _operandArr.pop(i)
                    i -= 1
                    break

    return _operandArr


def find_rez_arr(n):
    rez =   [''] * (2**n)

    for a in range(len(table)):
        table[a] = [rez]

    for i in range(len(rez)):
        bin_representation = str(bin(i))[2:]
        for j in range(n-len(bin_representation)):
            bin_representation = '0' + bin_representation
        rez[i] = list(bin_representation)

    return rez

def calculating():
    _operandArr = find_operand_arr()
    n = len(_operandArr)
    rez = find_rez_arr(n)

    const_instead_operand_arr = [2 ** n]
    for i in range(len(const_instead_operand_arr)):
        const_instead_operand_arr[i] = resultArr.copy()

        for k in range(len(const_instead_operand_arr[i])):
            index = _operandArr.index(const_instead_operand_arr[i][k])
            const_instead_operand_arr[i][k] = rez[i][index] if index>= 0 else None

    rez_elem_arr = []
    for q in range(len(const_instead_operand_arr)):
        rez_elem_arr.append(find_formula_rezult(const_instead_operand_arr[q]))
        return rez_elem_arr

def count_binary_operator_result(firstOperand, secondOperand, symbol):
    truthTable = TRUTH_TABLE_BINARY[symbol]

    for row in truthTable:
        if firstOperand == truthTable[row][0]:
            if secondOperand == truthTable[row][1]:
                return truthTable[row][2]

def count_unary_operator_result(operand, symbol):
    truthTable = TRUTH_TABLE_UNARY[symbol]

    for row in range(len(truthTable)):
        if operand == truthTable[row][0]:
            return truthTable[row][1]

def find_formula_rezult(array):
    arr = array.copy()
    for i in range(len(arr)):
        if arr[i] in GRAMMAR['bin_operation']:
            arr[i-2] = count_binary_operator_result(arr[i-2], arr[i-1], arr[i])
            arr.pop(i-1)
            arr.pop(i-1)
            i -= 2
        elif arr[i] in GRAMMAR['unar_operation']:
            arr[i-1] = count_unary_operator_result(arr[i-1], arr[i])
            arr.pop(i)
            i -= 1
        i += 1
    return arr
