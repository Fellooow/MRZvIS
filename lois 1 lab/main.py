########################################################################################################
# Лабораторная работа #1 по дисциплине ЛОИС                                                            #
# Выполнена студентом группы 021703 БГУИР Колосовским Егором Сергеевичем                               #
# Файл содержит функции подсчета количества подформул в формуле сокращенного языка логики высказываний #
# 2023.03.21 v0.0.1                                                                                    #
########################################################################################################


from GetNumberOfSubformulas import FormulaChecker, search
import CheckFormula


def main():
    parse = FormulaChecker()
    neutral = CheckFormula

    input_string = ""

    while input_string != "exit":
        input_string = input("Input formula to find subformulas: ")
    # input_string = "(A/\B)"
        if input_string != "exit":
            if parse.is_formula(input_string):
            # print('Number of subformulas: ', search_subformulas(input_string))
                print('Number of subformulas: ', search(parse, input_string))
            else:
                print("Invalid formula")

        # input_string = input("Input formula to check: ")
        # if input_string != "exit":
        #     neutral.check_is_neutral(input_string)


if __name__ == "__main__":
    main()
