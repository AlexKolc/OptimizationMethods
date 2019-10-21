import time
import math


# import matplotlib.pyplot as plt
# import pylab


def f(x):
    return math.pow((x - 15), 2) + 5
    # return math.pow(x + 5, 4)
    # return math.sin(x)


def F(n):
    return 1 / math.sqrt(5) * (math.pow((1 + math.sqrt(5)) / 2, n)
                               - math.pow((1 - math.sqrt(5)) / 2, n))


# PART I

def dichotomyMethod(a, b, eps):
    delta = eps / 2
    iterations = 0
    while math.fabs(b - a) > eps:
        iterations += 1
        x = (a + b) / 2
        f1 = f(x - delta)
        f2 = f(x + delta)
        if f1 < f2:  # if need finding max, exchange to '>'
            b = x
        else:
            a = x
    x = (a + b) / 2
    print("Iterations = %s" % iterations)
    return x


def goldenRatioMethod(a, b, eps):
    iterations = 0
    x1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
    x2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
    f1 = f(x1)
    f2 = f(x2)
    while math.fabs(b - a) > eps:
        iterations += 1
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
    print("Iterations = %s" % iterations)
    return x


def fibonacciMethod(a, b, eps):
    n = math.ceil(math.log2(math.sqrt(5) * (b - a) / eps) / math.log2((1 + math.sqrt(5)) / 2)) - 2
    iterations = 0
    x1 = a + F(n) / F(n + 2) * (b - 2)
    x2 = a + F(n + 1) / F(n + 2) * (b - 2)
    f1 = f(x1)
    f2 = f(x2)
    k = 1
    while k < n:
        iterations += 1
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + F(n - k + 1) / F(n - k + 3) * (b - a)
            f1 = f(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + F(n - k + 2) / F(n - k + 3) * (b - a)
            f2 = f(x2)
        k += 1
    x = (a + b) / 2
    print("Iterations = %s" % iterations)
    return x


def minFunctionOnLineSearch(eps):
    delta = eps / 2
    x0 = 1

    f0 = f(x0 - delta)
    f1 = f(x0)
    f2 = f(x0 + delta)

    if f1 > f2:
        x_next = x0
        h = delta
    elif f1 > f0:
        x_next = x0
        h = -delta
    else:
        return "min in %s" % x0

    h *= 2
    x_next += h
    f1, f2 = f(x_next - h), f(x_next)
    while f1 > f2:
        h *= 2
        x_next += h
        f1, f2 = f2, f(x_next)

    if x_next - h - h / 2 < x_next:
        return "[%s, %s]" % (x_next - h - h / 2, x_next)
    else:
        return "[%s, %s]" % (x_next, x_next - h - h / 2)


def main():
    # INITIALIZATION
    a, b = 2, 200
    # a, b = -10, 15
    # a, b = -math.pi / 2, math.pi / 2
    eps = 1e-3

    print("Dichotomy method: ", dichotomyMethod(a, b, eps))
    print("Golden ratio method: ", goldenRatioMethod(a, b, eps))
    print("Fibonacci method:", fibonacciMethod(a, b, eps))
    print("Search the minimum function on line:", minFunctionOnLineSearch(eps))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
