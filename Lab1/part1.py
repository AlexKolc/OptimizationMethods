import math


def f(x):
    return math.pow((x - 15), 2) + 5
    #return math.pow(x + 5, 4)
    #return math.sin(x)


def F(n):
    return 1 / math.sqrt(5) * (math.pow((1 + math.sqrt(5)) / 2, n)
                               - math.pow((1 - math.sqrt(5)) / 2, n))


# PART I

def dichotomyMethod(a, b, eps):
    iterations = 0
    while math.fabs(b - a) > eps:
        iterations += 1
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


def fibonacciMethod(a, b, eps):
    n = math.ceil(math.log2(math.sqrt(5) * (b - a) / eps) / math.log2((1 + math.sqrt(5)) / 2)) - 2

    # num = int(math.ceil(math.log((math.sqrt(5) * (b - a)) / (eps * (3 + math.sqrt(5))), (1 + math.sqrt(5)) / 2)))
    #
    # n_iter = 0
    #
    # while F(n_iter + 2) < (b - a) / eps:
    #     n_iter += 1
    #
    # print(n, num, n_iter)

    k = 1
    while k < n:
        x1 = a + F(n - k + 1) / F(n - k + 3) * (b - a)
        x2 = a + F(n - k + 2) / F(n - k + 3) * (b - a)
        if f(x1) < f(x2):
            b = x2
        else:
            a = x1
        k += 1
    x = (a + b) / 2
    return f(x)


def minFunctionOnLineSearch():
    return


def main():
    # INITIALIZATION
    a, b = 2, 200
    #a, b = -10, 15
    #a, b = -math.pi / 2, math.pi / 2

    print("Dichotomy method: ", dichotomyMethod(a, b, eps))
    print("Golden ratio method: ", goldenRatioMethod(a, b, eps))
    print("Fibonacci method", fibonacciMethod(a, b, eps))


if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
