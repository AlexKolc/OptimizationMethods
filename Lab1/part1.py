import math


# FUNCTION

def f(x):
    return math.pow(x + 5, 4)
    #return math.sin(x)


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
    phi = (1 + math.sqrt(5)) / 2
    while math.fabs(b - a) > eps:
        x1 = b - (b - a) / phi
        x2 = a + (b - a) / phi
        if f(x1) < f(x2):
            b = x2
        else:
            a = x1
    x = (a + b) / 2
    return f(x)


def fibonacciMethod():
    return


def minFunctionOnLineSearch():
    return


def main():
    # INITIALIZATION
    a, b = -10, 15
    #a = -math.pi / 2
    #b = math.pi / 2
    eps = 1e-3

    print("Dichotomy method: ", dichotomyMethod(a, b, eps))
    print("Golden ratio method: ", goldenRatioMethod(a, b, eps))


if __name__ == '__main__':
    main()
