######################################################################
# Лабораторная работа #2 по дисциплине ЛОИС                          #
# Выполнена студентом группы 021703 БГУИР Колосовский Егор Сергеевич #
# Программа проверки формулы на нейтральность                        #
#                                                                    #
# 2023.04.25 v0.0.3                                                  #
######################################################################


from CheckFormula import *


class FormulaResolver:
    def __init__(self, test_resolver=False):
        self.syntax = Syntax()

    def resolve_formula_truth_table(self, formula: Formula):
        variables = self.get_all_variables_in_formula(formula)
        table = []
        range_right = len(variables) * len(variables)
        if len(variables) == 1:
            range_right = 2
        if len(variables) == 0:
            range_right = 1
        for i in range(0, range_right):
            str_variables = bin(i)[2:].rjust(len(variables), '0')
            # print(str_variables)
            values = list(str_variables)
            values = [int(item) for item in values]
            variables_with_values = dict(zip(variables, values))
            result = self.resolve_formula_with_variables(formula.vertexes[1], formula, variables_with_values)
            # print(variables_with_values, result)
            table.append((variables_with_values, result))
        return table

    def resolve_formula_with_variables(self, vertex, formula: Formula, variables: dict):
        if vertex.vertex_type == "constant":
            # print(f"{vertex.content}: {int(vertex.content)}")
            return int(vertex.content)
        if vertex.vertex_type == "atomic_formula":
            # print(f"{vertex.content}: {variables[vertex.content]}")
            return variables[vertex.content]
        if vertex.vertex_type == "unary_complex_formula":
            children_indexes = [edge.child_vertex_index for edge in formula.edges if edge.parent_vertex_index == vertex.index]
            variable = self.resolve_formula_with_variables(formula.vertexes[children_indexes[0]], formula, variables)
            # print(f"{vertex.content}: {self.negation(variable)}")
            return self.negation(variable)
        if vertex.vertex_type == "binary_complex_formula":
            children_indexes = [edge.child_vertex_index for edge in formula.edges if edge.parent_vertex_index == vertex.index]
            variable_1 = self.resolve_formula_with_variables(formula.vertexes[children_indexes[0]], formula, variables)
            variable_2 = self.resolve_formula_with_variables(formula.vertexes[children_indexes[1]], formula, variables)
            start_char = 1 + len(formula.vertexes[children_indexes[0]].content)
            finish_char = -1 - len(formula.vertexes[children_indexes[1]].content)
            formula_func = vertex.content[start_char:finish_char]

            if formula_func == self.syntax.conjunction:
                # print(f"{vertex.content}: {self.conjunction(variable_1, variable_2)}")
                return self.conjunction(variable_1, variable_2)
            if formula_func == self.syntax.disjunction:
                # print(f"{vertex.content}: {self.disjunction(variable_1, variable_2)}")
                return self.disjunction(variable_1, variable_2)
            if formula_func == self.syntax.implication:
                # print(f"{vertex.content}: {self.implication(variable_1, variable_2)}")
                return self.implication(variable_1, variable_2)
            if formula_func == self.syntax.equivalence:
                # print(f"{vertex.content}: {self.equivalence(variable_1, variable_2)}")
                return self.equivalence(variable_1, variable_2)
        raise Exception("The formula cannot be resolved.")

    def get_all_variables_in_formula(self, formula: Formula):
        variables = []
        for vertex in formula.vertexes:
            if vertex.vertex_type == "atomic_formula":
                if vertex.content not in self.syntax.constants and vertex.content not in variables:
                    variables.append(vertex.content)
        return list(variables)

    def negation(self, variable: int):
        if variable == 0:
            return 1
        return 0

    def conjunction(self, variable_1: int, variable_2: int):
        if variable_1 == 0 or variable_2 == 0:
            return 0
        return 1

    def disjunction(self, variable_1: int, variable_2: int):
        if variable_1 == 1 or variable_2 == 1:
            return 1
        return 0

    def implication(self, variable_1: int, variable_2: int):
        if variable_1 == variable_2 or variable_1 == 0:
            return 1
        return 0

    def equivalence(self, variable_1: int, variable_2: int):
        if variable_1 == variable_2:
            return 1
        return 0

    # ### OTHER
    def formula_is_neutral(self, formula: Formula):
        table = self.resolve_formula_truth_table(formula)
        bool_one = False
        bool_zero = False
        for res in table:
            if res[1] == 1:
                bool_one = True
            if res[1] == 0:
                bool_zero = True
            if bool_one and bool_zero:
                print('Formula is neutral')
                return True
        print("Formula isn't neutral")
        return False

