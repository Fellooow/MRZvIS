#######################################################################################################
# Лабораторная работа #1 по дисциплине ЛОИС                                                           #
# Выполнена студентом группы 021703 БГУИР Колосовским Егором Сергеевичем                              #
# Файл содержит функции подсчета количества подформул в формуле сокращенного языка логики высказываний#
# 2023.03.21 v0.0.1                                                                                   #
#######################################################################################################


# def count_subformulas():
#     input_formula = input("Enter a formula: ")
#     if verify_formula(input_formula):
#         print("Number of subformulas:", search_subformulas(input_formula))
#     else:
#         print("Invalid formula")
#
# def verify_formula(formula):
#     unary_operators = ["!"]
#     binary_operators = ["/\\", "\/", "->", "~"]
#     stack = []
#     for char in formula:
#         if char.isupper() or char == "0" or char == "1":
#             stack.append(char)
#         elif char in unary_operators:
#             if len(stack) == 0 or not stack[-1].isupper() and stack[-1] != "0" and stack[-1] != "1":
#                 return False
#         elif char in binary_operators:
#             if len(stack) < 2 or not stack[-1].isupper() and stack[-1] != "0" and stack[-1] != "1" or not stack[-2].isupper() and stack[-2] != "0" and stack[-2] != "1":
#                 return False
#             stack.pop()
#         elif char == "(":
#             stack.append(char)
#         elif char == ")":
#             if len(stack) == 0 or stack[-1] != "(":
#                 return False
#             stack.pop()
#     return len(stack) == 1 and (stack[-1].isupper() or stack[-1] == "0" or stack[-1] == "1")
#
# def search_subformulas(formula):
#     stack = []
#     subformulas = set()
#     for char in formula:
#         if char == "(":
#             stack.append("")
#         elif char == ")":
#             subformulas.add(stack.pop())
#         elif char.isupper() or char == "0" or char == "1":
#             if len(stack) == 0:
#                 subformulas.add(char)
#             else:
#                 stack[-1] += char
#         elif char in ["!", "/\\", "\/", "-", ">"]:
#             stack[-1] += char
#     return len(subformulas)

replaceFormula = "R"
tempFormula = ""
atomOrConstant = "ABCDEFGHIJKLMNOPQRSTUVWXYZ01"

class Controller:
    def checkBracket(self, expression):
        queueBracket = []
        for digit in expression:
            if digit == "(":
                queueBracket.append("(")
            elif digit == ")":
                leftBracket = queueBracket.pop() if queueBracket else None
                if leftBracket != "(" or leftBracket is None:
                    return False
        return len(queueBracket) == 0

    def isFormula(self, expression):
        global tempFormula
        formula = expression
        while formula != tempFormula:
            tempFormula = formula
            for op in ["!", "&", "|", "->", "~"]:
                for c in atomOrConstant:
                    unary = "({}!)".format(c)
                    binary = "({}{}{})".format(c, op, c)
                    pattern = unary + "|" + binary
                    formula = formula.replace(pattern, replaceFormula)
        tempFormula = ""
        return len(formula) == 1

    def getNumberOfSubformulas(self, formula):
        result = []
        oldFormule = ""
        leftFormule = ""
        result.append(formula)
        while formula != replaceFormula:
            for op in ["!", "&", "|", "->", "~"]:
                for c in atomOrConstant:
                    unary = "({}!)".format(c)
                    binary = "({}{}{})".format(c, op, c)
                    pattern = unary + "|" + binary
                    subformula = result[-1]
                    if subformula.find(replaceFormula) == -1:
                        break
                    subformula = subformula.replace(replaceFormula, oldFormule, 1)
                    if subformula.find(replaceFormula) == -1:
                        break
                    subformula = subformula.replace(replaceFormula, leftFormule, 1)
                    if subformula.find(replaceFormula) == -1:
                        break
                    result.append(subformula.replace(pattern, replaceFormula, 1))
            if len(result[-1]) == 1:
                break
            subformula = result.pop()
            oldFormule = subformula if oldFormule == "" else oldFormule
            leftFormule = oldFormule if leftFormule == "" else leftFormule
        result = list(set(result))
        return len(result)



while True:
    input_formula = input('Input formula: ')
    c = Controller()
    c.checkBracket(input_formula)
    c.isFormula(input_formula)
    c.getNumberOfSubformulas(input_formula)
