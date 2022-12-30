//
// Created by Egor on 14.12.2022.
//

#ifndef MRZ2_NET_H
#define MRZ2_NET_H

#pragma once

#include <iostream>
#include <cmath>
#include "armadillo-11.4.2\include\armadillo"


using namespace std;
using namespace arma;

#define alpha 0.1
#define ALPHA 0.00001
#define E_BASE 0.0001
#define ITERS 1000000

class Elman
{
public:
    Elman();
    void startLearning();
    void generatePredictedSequence();

private:

    vector<double> sequence;    //исходная последовательность
    vector<double> resultSequence;    //Выходная последовательность
    vector<double> expectedSequence;    //Ожидаемая выходная последовательность
    int k;  //Размерность обучаемой последовательности
    int row;  //Количество столбцов в матрице обучения - размер окна
    int num_hide_neuron;  //Количество образов или количество нейронов скрытого слоя
    double max_error; //Максимальная допустимая ошибка
    double alfa; //Коэффициент альфа
    double alpa; //Коэффициент альфа для функции активации
    int N; //Максимальное количество шагов обучения
    int num_predict_elements; //Количество предсказываемых элементов

    vec input;   //Входной вектор (row)
    vec hidden;   //Выходной вектор из скрытого слоя (num_hide_neuron)
    double output{};  //Выходной вектор из выходного слоя (1)
    vec context_hidden;   //Контекстный слой для скрытого слоя (num_hide_neuron)
    double context_output{};    //Контекстный слой для выходного слоя (1)
    mat X;  //Матрица обучения num_hide_neuron x row
    mat W;  //Матрица весов W на скрытом слое row x num_hide_neuron
    mat Wch_h;  //Матрица весов между контекстным с предыдущими значениями скрытого и скрытым слоем num_hide_neuron x num_hide_neuron
    mat W_; //Матрица весов W_ на выходном слое num_hide_neuron x 1
    mat Wco_h; //Матрица весов между контекстным с предыдущим значением выходного и скрытым слоем 1 x num_hide_neuron
    vec T;  //Пороговые значения для скрытого слоя
    double T_{};  //Пороговые значения для выходного слоя

    vector<double> expectedValues;   //Значения, которые необходимо получить при обучении для каждого входного вектора
    void enterInputParameters();
    void showInputParameters() const;
    [[nodiscard]] bool checkInputParameters() const;
    void printSequence();
    void createMatrices();
    [[nodiscard]] double ELU(double x) const;
    double activateFunction(double x);
    double derOfActivateFunction(double x);
    void directErrorProp();
    void backErrorProp(double val);
    static vector<double> calculateFibonacci(int num);
    static vector<double> calculateFactorial(int num);
    static vector<double> calculatePeriodic(int num);
    static vector<double> calculatePower(int num);
    static vector<double> calculateNaturalNumbers(int num);
};

#endif //MRZ2_NET_H
