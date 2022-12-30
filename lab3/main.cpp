#include <iostream>
#include "net.h"

void main()
{
    Elman net;
    net.startLearning();
    net.generatePredictedSequence();
    system("pause");
    return;
}
