######################################################################
# Лабораторная работа #2 по дисциплине ЛОИС                          #
# Выполнена студентом группы 021703 БГУИР Колосовский Егор Сергеевич #
# Программа проверки формулы на нейтральность                        #
#                                                                    #
# 2023.04.25 v0.0.1                                                  #
######################################################################


from CheckFormula import FormulaCheck
from ResolveFormula import FormulaResolver


def main():
    parse = FormulaCheck()
    resolve = FormulaResolver()

    input_string = ""
    
    while input_string != "exit":
        input_string = input("Input formula: ")
        if input_string != "exit":
            if parse.is_formula(input_string):
                print(resolve.formula_is_neutral(parse.formulas[input_string]))

            else:
                print('Invalid formula')


if __name__ == "__main__":
    main()
