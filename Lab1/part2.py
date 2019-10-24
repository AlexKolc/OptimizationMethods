import time
import math
import matplotlib.pyplot as plt
from beautifultable import BeautifulTable
from mpl_toolkits.mplot3d import axes3d
import numpy as np


def F(n):
    return 1 / math.sqrt(5) * (math.pow((1 + math.sqrt(5)) / 2, n)
                               - math.pow((1 - math.sqrt(5)) / 2, n))


def plotFunction():
    ax = axes3d.Axes3D(plt.figure())
    X = np.arange(-100, 100, 1)
    Y = np.arange(-100, 100, 1)
    Z = np.zeros((X.size, Y.size))
    for i in range(0, X.size):
        for j in range(0, Y.size):
            Z[i][j] = f([X[i], Y[j]])

    ax.plot_wireframe(X, Y, Z)
    # ax.plot_surface(X, Y, Z)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.show()


class Table:
    def __init__(self, length):
        self.table = BeautifulTable()
        self.length = length
        self.table.column_headers = ["k", "Интервал неопределенности"
            , "Соотношение длин", "x1", "f(x1)"
            , "x2", "f(x2)"]

    def addRow(self, k, a, b, x1, f1, x2, f2):
        if x1 != "-":
            self.table.append_row([k, "(%s, %s)" % (round(a, 3), round(b, 3))
                                      , round((b - a) / self.length, 3), round(x1, 3)
                                      , round(f1, 4), round(x2, 3), round(f2, 4)])
        else:
            self.table.append_row([k, "(%s, %s)" % (round(a, 3), round(b, 3))
                                      , x1, x1, f1, x2, f2])

    def printToFile(self, fileName):
        with open(fileName, 'w') as file:
            print(self.table, file=file)


# PART II

def dichotomyMethod(a, b, eps, x, s):
    # table = Table(b - a)
    # print("Iterations by math = %s" % math.ceil(math.log2((b - a) / eps)))
    delta = eps / 2
    iterations = 0
    while math.fabs(b - a) > eps:
        iterations += 1
        lam = (a + b) / 2
        lam1 = lam - delta
        lam2 = lam + delta
        g1 = g(lam1, x, s)
        g2 = g(lam2, x, s)
        # table.addRow(iterations, a, b, lam1, g1, lam2, g2)
        if g1 < g2:  # if need finding malam, exchange to '>'
            b = lam
        else:
            a = lam
    lam = (a + b) / 2
    return lam


def goldenRatioMethod(a, b, eps, x, s):
    # print("Iterations by math = %s" % math.ceil(math.log2((b - a) / eps) / math.log2((math.sqrt(5) + 1) / 2)))
    # table = Table(b - a)
    iterations = 0
    lam1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
    lam2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
    g1 = g(lam1, x, s)
    g2 = g(lam2, x, s)
    while math.fabs(b - a) > eps:
        iterations += 1
        # table.addRow(iterations, a, b, lam1, g1, lam2, g2)
        if g1 < g2:
            b = lam2
            lam2 = lam1
            g2 = g1
            lam1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
            g1 = g(lam1, x, s)
        else:
            a = lam1
            lam1 = lam2
            g1 = g2
            lam2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
            g2 = g(lam2, x, s)
    # table.addRow(iterations + 1, a, b, "-", "-", "-", "-")
    # table.printToFile("goldenRatio.txt")
    lam = (a + b) / 2
    # print("Iterations = %s" % iterations)
    return lam


def fibonacciMethod(a, b, eps, x, s):
    n = math.ceil(math.log2(math.sqrt(5) * (b - a) / eps) / math.log2((1 + math.sqrt(5)) / 2)) - 2
    # print("Iterations by math = %s" % n)
    # table = Table(b - a)
    iterations = 0
    lam1 = a + F(n) / F(n + 2) * (b - 2)
    lam2 = a + F(n + 1) / F(n + 2) * (b - 2)
    g1 = g(lam1, x, s)
    g2 = g(lam2, x, s)
    k = 1
    while k < n:
        iterations += 1
        # table.addRow(iterations, a, b, lam1, g1, lam2, g2)
        if g1 < g2:
            b = lam2
            lam2 = lam1
            g2 = g1
            lam1 = a + F(n - k + 1) / F(n - k + 3) * (b - a)
            g1 = g(lam1, x, s)
        else:
            a = lam1
            lam1 = lam2
            g1 = g2
            lam2 = a + F(n - k + 2) / F(n - k + 3) * (b - a)
            g2 = g(lam2, x, s)
        k += 1
    # table.addRow(iterations + 1, a, b, "-", "-", "-", "-")
    # table.printToFile("fibonacci.txt")
    lam = (a + b) / 2
    return lam


def minFunctionOnLineSearch(x, s, eps):
    delta = eps / 2
    lam0 = 1

    g0 = g(lam0 - delta, x, s)
    g1 = g(lam0, x, s)
    g2 = g(lam0 + delta, x, s)

    if g1 > g2:
        lam_next = lam0
        h = delta
    elif g1 > g0:
        lam_next = lam0
        h = -delta
    else:
        return "min in %s" % lam0

    h *= 2
    lam_next += h
    g1, g2 = g(lam_next - h, x, s), g(lam_next, x, s)
    while g1 > g2:
        h *= 2
        lam_next += h
        g1, g2 = g2, g(lam_next, x, s)

    if lam_next - h - h / 2 < lam_next:
        return [lam_next - h - h / 2, lam_next]
    else:
        return [lam_next, lam_next - h - h / 2]


def fastestDescentMethod(x1, eps):
    s = grad(x1)
    print("Grad =", s)
    a = minFunctionOnLineSearch(x1, s, eps)
    b, a = a[1], a[0]
    print("(%s, %s)" % (a, b))
    lam = goldenRatioMethod(a, b, eps, x1, s)
    print("Lambda= ", lam)
    x2 = []
    for i in range(0, len(x1)):
        x2.append(x1[i] + lam * s[i])
    print("Next x= ", x2)
    f1 = f(x1)
    f2 = f(x2)
    while math.fabs(f2 - f1) > eps:
        x1 = x2
        f1 = f2
        s = grad(x1)
        print("Grad= ", s)
        a = minFunctionOnLineSearch(x1, s, eps)
        b, a = a[1], a[0]
        print("(%s, %s)" % (a, b))
        lam = goldenRatioMethod(a, b, eps, x1, s)
        print("Lambda =", lam)
        x2 = []
        for i in range(0, len(x1)):
            x2.append(x1[i] + lam * s[i])
        print("Next x =", x2)
        f2 = f(x2)
    return x2

    # directional vector from M0(x1, x2, ..., xn)


def grad(x):
    zx1 = 2 * x[0] + math.exp(x[0] + x[1])
    zx2 = 4 * x[1] + math.exp(x[0] + x[1])
    return [-zx1, -zx2]

    # zx1 = 2 * x[0] * (math.pow(x[1], 6)
    #                   + math.pow(x[1], 4)
    #                   - 2 * math.pow(x[1], 3)
    #                   - math.pow(x[1], 2)
    #                   - 2 * x[1] + 3
    #                   ) + 5.25 * math.pow(x[1], 3) \
    #       + 4.5 * math.pow(x[1], 2) + 3 * x[1] - 12.75
    #
    # zx2 = x[0] * (x[0] * (6 * math.pow(x[1], 5)
    #                       + 4 * math.pow(x[1], 3)
    #                       - 6 * math.pow(x[1], 2)
    #                       - 2 * x[1] - 2)
    #               + 15.75 * math.pow(x[1], 2) + 3)
    # return [-zx1, -zx2]


# global min at (x, y) = (3, 1/2) (WOLFRAM)
def f(x):
    return x[0] ** 2 + 2 * x[1] ** 2 + math.exp(x[0] + x[1])

    # return (1.5 - x[0] * (1 - x[1])) ** 2 \
    #        + (2.25 - x[0] * (1 - x[1] * x[1])) ** 2 \
    #        + (2.625 - x[0] * (1 - x[1] * x[1] * x[1])) ** 2


def g(lam, x, s):
    return (x[0] + lam * s[0]) ** 2 + 2 * (x[1] + lam * s[1]) ** 2 + math.exp((x[0] + lam * s[0]) + (x[1] + lam * s[1]))

    # return (1.5 - (x[0] + lam * s[0]) * (1 - (x[1] + lam * s[1]))) ** 2 \
    #        + (2.25 - (x[0] + lam * s[0]) * (1 - (x[1] + lam * s[1]) ** 2)) ** 2 \
    #        + (2.625 - (x[0] + lam * s[0]) * (1 - math.pow((x[1] + lam * s[1]), 3))) ** 2


def main():
    # INITIALIZATION

    # plotFunction()

    x = [0, 0]
    eps = 1e-5
    print(fastestDescentMethod(x, eps))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
