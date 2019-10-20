import math


# FUNCTION

def f(x):
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


def goldenRatioMethod():

    return


def fibonacciMethod():
    return


def minFunctionOnLineSearch():
    return


def main():
    # INITIALIZATION
    a = -math.pi / 2
    b = math.pi / 2
    eps = 1e-3

    print("Dichotomy method: ", dichotomyMethod(a, b, eps))


if __name__ == '__main__':
    main()
