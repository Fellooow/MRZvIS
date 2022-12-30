//
// Created by Egor on 14.12.2022.
//

#include "net.h"


Elman::Elman()
{
    int key;
    cout << "Choose sequence: \n"
         << "1. Fibonacci: \n0,1,1,2,3,5,8,13,21,34,55,89,144,...\n"
         << "2. Factorial: \n1,2,6,24,120,720,5040,40320,...\n"
         << "3. Periodic: \n1,0,1,0,1,0,1,...\n"
         << "4. Power: \n1,4,9,16,25,36,49,64,81,...\n"
         << "5. Natural numbers: \n1,2,3,4,5,6,7,8,...\n";

    cin >> key;
    switch (key) {
        case 1: {
            int num;
            cout << "Enter amount of elements: 3<=n<=7\n";
            cin >> num;
            if (num < 3 || num > 7) {
                cout << "Incorrect data!";
                return;
            }
            k = num;
            sequence = calculateFibonacci(num);
            printSequence();
            int key;
            cout << "\n1 - For use standard parameters \n"
                    "2 - For enter yours \n";
            cin >> key;
            if (key == 1) {
                row = 2;
                num_hide_neuron = k - row;
                alfa = ALPHA;
                max_error = E_BASE;
                N = ITERS;
                showInputParameters();
            }
            else if (key == 2) {
                enterInputParameters();
            }
            else
            {
                cout << "Incorrect data!";
                return;
            }
            cout << "Number of elements to predict: 1<=n<=2\n";
            cin >> num;
            if (num < 1 || num > 2) {
                cout << "Incorrect data!";
                return;
            }
            num_predict_elements = num;
            expectedSequence = calculateFibonacci(k + num_predict_elements);
            break;
        }
        case 2: {
            int num;
            cout << "Number of elements: 4<=n<=5\n";
            cin >> num;
            if (num < 4 || num > 5) {
                cout << "Incorrect data!";
                return;
            }
            k = num;
            sequence = calculateFactorial(num);
            printSequence();
            int key;
            cout << "\n1 - For use standard parameters \n"
                    "2 - For enter yours \n";
            cin >> key;
            if (key == 1) {
                row = 3;
                num_hide_neuron = k - row;
                alfa = ALPHA;
                max_error = E_BASE;
                N = ITERS;
                showInputParameters();
            }
            else if (key == 2) {
                enterInputParameters();
            }
            else
            {
                cout << "Incorrect data!";
                return;
            }
            cout << "Number of elements to predict: 1\n";
            cin >> num;
            if (num < 1 || num > 1) {
                cout << "Incorrect data!";
                return;
            }
            num_predict_elements = num;
            expectedSequence = calculateFactorial(k + num_predict_elements);
            break;
        }
        case 3: {
            int num;
            cout << "Number of elements: 5<=n<=6\n";
            cin >> num;
            if (num < 5 || num > 6) {
                cout << "Incorrect data!";
                return;
            }
            k = num;
            sequence = calculatePeriodic(num);
            printSequence();
            int key;
            cout << "\n1 - For use standard parameters \n"
                    "2 - For enter yours \n";
            cin >> key;
            if (key == 1) {
                row = 4;
                num_hide_neuron = k - row;
                alfa = ALPHA;
                max_error = E_BASE;
                N = ITERS;
                showInputParameters();
            }
            else if (key == 2) {
                enterInputParameters();
            }
            else
            {
                cout << "Incorrect data!";
                return;
            }
            cout << "Number of elements to predict: 1<=n<=3\n";
            cin >> num;
            if (num < 1 || num > 3) {
                cout << "Incorrect data!";
                return;
            }
            num_predict_elements = num;
            expectedSequence = calculatePeriodic(k + num_predict_elements);
            break;
        }
        case 4: {
            int num;
            cout << "Number of elements: 4<=n<=6\n";
            cin >> num;
            if (num < 4 || num > 6) {
                cout << "Incorrect data!";
                return;
            }
            k = num;
            sequence = calculatePower(num);
            printSequence();
            int key;
            cout << "\n1 - For use standard parameters \n"
                    "2 - For enter yours \n";
            cin >> key;
            if (key == 1) {
                row = 3;
                num_hide_neuron = k - row;
                alfa = ALPHA;
                max_error = E_BASE;
                N = ITERS;
                showInputParameters();
            }
            else if (key == 2) {
                enterInputParameters();
            }
            else
            {
                cout << "Incorrect data!";
                return;
            }
            cout << "Number of elements to predict: 1<=n<=6\n";
            cin >> num;
            if (num < 1 || num > 10) {
                cout << "Incorrect data!";
                return;
            }
            num_predict_elements = num;
            expectedSequence = calculatePower(k + num_predict_elements);
            break;
        }
        case 5: {
            int num;
            cout << "Number of elements: 3<=n<=15\n";
            cin >> num;
            if (num < 3 || num > 15) {
                cout << "Incorrect data!";
                return;
            }
            k = num;
            sequence = calculateNaturalNumbers(num);
            printSequence();
            int key;
            cout << "\n1 - For use standard parameters \n"
                    "2 - For enter yours \n";
            cin >> key;
            if (key == 1) {
                row = 2;
                num_hide_neuron = k - row;
                alfa = ALPHA;
                max_error = E_BASE;
                N = ITERS;
                showInputParameters();
            }
            else if (key == 2) {
                enterInputParameters();
            }
            else
            {
                cout << "Incorrect data!";
                return;
            }
            cout << "Number of elements to predict: 1<=n<=10\n";
            cin >> num;
            if (num < 1 || num > 10) {
                cout << "Incorrect data!";
                return;
            }
            num_predict_elements = num;
            expectedSequence = calculateNaturalNumbers(k + num_predict_elements);
            break;
        }
        default: {
            printf("Something go wrong!\n");
            return;
        }
    }
    if (!checkInputParameters())
        return;
    createMatrices();
}


void Elman::enterInputParameters()
{
    cout << "\nEnter window size(row) (row>=1 & row<k)\n";
    cin >> row;
    num_hide_neuron = k - row;
    cout << "Enter max error(max_error) (0<max_error<=0.1)\n";
    cin >> max_error;
    cout << "Enter learning step (alfa) (0<alfa<=0.1 & alfa<=max_error)\n";
    cin >> alfa;
    cout << "Enter max number of learning steps(N)(1<=N<=1000000)\n";
    cin >> N;
}


void Elman::showInputParameters() const
{
    cout << "Window size row = " << row << "\n";
    cout << "Number of images in the training sample num_hide_neuron = " << num_hide_neuron << "\n";
    cout << "Max error max_error = " << max_error << "\n";
    cout << "Learning step alfa = " << alfa << "\n";
    cout << "Max number of learning steps N = " << N << "\n";
}


bool Elman::checkInputParameters() const
{
    if (row <= 0 || row >= k || max_error <= 0 || max_error > 0.1 || alfa <= 0 || alfa > 0.1 || N < 1 || N > 1000000) {
        cout << "Incorrect data!";
        return false;
    }
    return true;

}


void Elman::printSequence()
{
    cout << "Learning sequence: \n";
    for (int i = 0; i < k; i++)
    {
        cout << sequence[i];
        if (i < k - 1)
            cout << ", ";
    }
}


vector<double> Elman::calculateFibonacci(int num)
{
    vector<double> seq;
    seq.push_back(0);
    seq.push_back(0.01);
    for (int i = 1; i < num; i++)
    {
        seq.push_back(seq[i] + seq[i - 1]);
    }

    return seq;
}


vector<double> Elman::calculateFactorial(int num)
{
    vector<double> seq;
    double x = 1;

    for (int i = 1; i <= num; i++) {
        for (int j = 1; j <= i; j++)
            x *= j;
        seq.push_back(x / 1000.0);
        x = 1;
    }

    return seq;
}


vector<double> Elman::calculatePeriodic(int num)
{
    vector<double> seq;

    for (int i = 0; i < num; i++)
    {
        switch (i % 4) {
            case 0: {
                seq.push_back(1);
                break;
            }
            case 1: {
                seq.push_back(0);
                break;
            }
            case 2: {
                seq.push_back(1);
                break;
            }
            case 3: {
                seq.push_back(0);
                break;
            }
        }
    }

    return seq;
}


vector<double> Elman::calculatePower(int num)
{
    vector<double> seq;

    for (int i = 1; i <= num; i++)
    {
        seq.push_back(pow(i, 2) / 100);
    }

    return seq;
}


vector<double> Elman::calculateNaturalNumbers(int num)
{
    vector<double> seq;

    for (int i = 1; i <= num; i++)
    {
        seq.push_back(i / 10.0);

    }

    return seq;
}


double Elman::ELU(double x) const
{
    return (x > 0? x : alpa*(exp(x)-1));
}

double Elman::activateFunction(double x)
{

    return ELU(x);

//    return log(x + sqrt(x * x + 1));
}


double Elman::derOfActivateFunction(double x)
{
    //return (1. / sqrt(x * x + 1.));
//    return (1. / exp(x));
    return (x > 0? 1 : ELU(x) + alpa);

}


void Elman::createMatrices()
{
    printf("Create matrices\n");
    vec input(row);
    input.fill(0);
    this->input = input;
    vec hidden(num_hide_neuron);
    hidden.fill(0);
    this->hidden = hidden;
    output = 0;
    vec context_hidden(row);
    context_hidden.fill(0);
    this->context_hidden = context_hidden;
    context_output = 0;

    vec T(num_hide_neuron);
    T.fill(0);
    this->T = T;
    T_ = 0;

    mat X(num_hide_neuron, row);
    for (int i = 0; i < num_hide_neuron; i++)
    {
        for (int j = 0; j < row; j++)
        {
            X(i, j) = sequence[i + j];
        }
        expectedValues.push_back(sequence[i + row]);
    }
    this->X = X;

    W = randu<mat>(row, num_hide_neuron); //[0,1]
    W = (W * 2.0 - 1.0);  //[-1,1]

    Wch_h = randu<mat>(num_hide_neuron, num_hide_neuron); //[0,1]
    Wch_h = (Wch_h * 2.0 - 1.0);  //[-1,1]

    W_ = randu<mat>(num_hide_neuron, 1); //[0,1]
    W_ = (W_ * 2.0 - 1.0);  //[-1,1]

    Wco_h = randu<mat>(1, num_hide_neuron); //[0,1]
    Wco_h = (Wco_h * 2.0 - 1.0);  //[-1,1]

}


void Elman::startLearning()
{
    double E;
    int iteration = 0;

    do {
        iteration++;
        E = 0.0;
        for (int i = 0; i < num_hide_neuron; i++) {

            input = conv_to<vec>::from(X.row(i));

            directErrorProp();

            E += pow(output - expectedValues[i], 2);

            backErrorProp(expectedValues[i]);

        }
        if (iteration <= 10 || iteration % 10000 == 0)
            cout << "Iteration: " << iteration << " Error: " << E << endl;

    } while (E > max_error && iteration < N);

    cout << "Finish learning" << endl;
    cout << "Iterations = " << iteration << " \nError = " << E << endl;
}

void Elman::directErrorProp()
{
    double S;

    for (int j = 0; j < num_hide_neuron; j++) {
        S = 0.0;

        for (int i = 0; i < row; i++) {
            S += W(i, j) * input[i];
        }

        for (int i = 0; i < num_hide_neuron; i++) {
            S += Wch_h(i, j) * context_hidden[i];
        }

        S += Wco_h(0, j) * context_output;

        S -= T(j);

        hidden[j] = activateFunction(S);
    }

    S = 0.0;

    for (int i = 0; i < num_hide_neuron; i++) {
        S += W_(i, 0) * hidden[i];
    }

    S -= T_;

    output = activateFunction(S);

    for (int i = 0; i < num_hide_neuron; i++) {
        context_hidden[i] = hidden[i];
    }

    context_output = output;

}

void Elman::backErrorProp(double val)
{
    double diff = alfa * (output - val);

    for (int i = 0; i < num_hide_neuron; i++) {
        for (int j = 0; j < row; j++) {
            W(j, i) -= diff * derOfActivateFunction(hidden[i]) * input[j];
        }

        for (int j = 0; j < num_hide_neuron; j++) {
            Wch_h(j, i) -= diff * derOfActivateFunction(hidden[i]) * context_hidden[j];
        }

        W_(i, 0) -= diff * derOfActivateFunction(output) * hidden[i];
        Wco_h(0, i) -= diff * derOfActivateFunction(hidden[i]) * context_output;
        T(i) = diff * derOfActivateFunction(hidden[i]);
    }

    T_ = diff;
}

void Elman::generatePredictedSequence()
{
    resultSequence.clear();

    int j = k - row;
    for (int i = 0; i < row; i++)
    {
        input[i] = sequence[j];
        j++;
    }

    for (int i = 0; i < num_predict_elements; i++)
    {
        if (i > 0)
        {
            for (int j = 0; j < row - 1; j++)
            {
                input[j] = input[j + 1];
            }

            input[row - 1] = output;
        }

        cout << input << endl;

        directErrorProp();

        resultSequence.push_back(output);

    }

    cout << "Result sequence: \n";
    for (int i = 0; i < num_predict_elements; i++)
    {
        cout << "Result: " << resultSequence[i] << "  Expected value: " << expectedSequence[k + i] << "  Line error: " << expectedSequence[k + i] - resultSequence[i] << endl;
        //cout << "Result: " << expectedSequence[k + i] - resultSequence[i] << "  Expected value: " << expectedSequence[k + i] << "  Line error: " << resultSequence[i] << endl;

    }
}