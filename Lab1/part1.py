import math


# FUNCTION

def f(x):
    #return math.pow(x + 5, 4)
    return math.sin(x)


# PART I

def dichotomyMethod(a, b, eps):
    while math.fabs(b - a) > eps:
        x = (a + b) / 2
        f1 = f(x - eps)
        f2 = f(x + eps)
        if f1 < f2:  # if need finding max, exchange to '>'
            b = x
        else:
            a = x
    x = (a + b) / 2
    return f(x)


def goldenRatioMethod(a, b, eps):
    x1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
    x2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
    f1 = f(x1)
    f2 = f(x2)
    while math.fabs(b - a) > eps:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
            f1 = f(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
            f2 = f(x2)
    x = (a + b) / 2
    return f(x)


def fibonacciMethod():
    return


def minFunctionOnLineSearch():
    return


def main():
    # INITIALIZATION
    #a, b = -10, 15
    a, b = -math.pi / 2, math.pi / 2
    eps = 1e-3

    print("Dichotomy method: ", dichotomyMethod(a, b, eps))
    print("Golden ratio method: ", goldenRatioMethod(a, b, eps))


if __name__ == '__main__':
    main()
