import time
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from beautifultable import BeautifulTable
from mpl_toolkits.mplot3d import axes3d
import numpy as np


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

class Minimization:
    x = []
    s = []

    def plotFunction(self):
        ax = axes3d.Axes3D(plt.figure())
        X = np.arange(-100, 100, 1)
        Y = np.arange(-100, 100, 1)
        Z = np.zeros((X.size, Y.size))
        for i in range(0, X.size):
            for j in range(0, Y.size):
                Z[i][j] = self.__f([X[i], Y[j]])

        # ax.plot_wireframe(X, Y, Z)
        ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.xlabel('x1')
        plt.ylabel('x2')
        for angle in range(0, 360):
            ax.view_init(30, angle)
            plt.draw()
            plt.pause(.001)
        # plt.show()

    # global min at (x, y) = (3, 1/2) (WOLFRAM)
    def __f(self, x):
        return (1.5 - x[0] * (1 - x[1])) ** 2 \
               + (2.25 - x[0] * (1 - math.pow(x[1], 2))) ** 2 \
               + (2.625 - x[0] * (1 - math.pow(x[1], 3))) ** 2

    def __g(self, lam):
        x = self.x
        s = self.s
        return (1.5 - (x[0] + lam * s[0]) * (1 - (x[1] + lam * s[1]))) ** 2 \
               + (2.25 - (x[0] + lam * s[0]) * (
                1 - math.pow((x[1] + lam * s[1]), 2))) ** 2 \
               + (2.625 - (x[0] + lam * s[0]) * (
                1 - math.pow((x[1] + lam * s[1]), 3))) ** 2

    def __grad(self, x):
        zx1 = (2 * x[1] - 2) * (-x[0] * (1 - x[1]) + 1.5) + (
                2 * x[1] ** 2 - 2) * (-x[0] * (1 - x[1] ** 2) + 2.25) + (
                      2 * x[1] ** 3 - 2) * (-x[0] * (1 - x[1] ** 3) + 2.625)

        zx2 = 6 * x[0] * x[1] ** 2 * (-x[0] * (1 - x[1] ** 3) + 2.625) + 4 * \
              x[0] * x[1] * (
                      -x[0] * (1 - x[1] ** 2) + 2.25) + 2 * x[0] * (
                      -x[0] * (1 - x[1]) + 1.5)

        len = math.sqrt(zx1 ** 2 + zx2 ** 2)
        return [-zx1 / len, -zx2 / len]

    def __F(self, n):
        return 1 / math.sqrt(5) * (
                math.pow((1 + math.sqrt(5)) / 2, n)
                - math.pow((1 - math.sqrt(5)) / 2, n))

    def __dichotomyMethod(self, a, b, eps):
        delta = eps / 2
        iterations = 0
        while math.fabs(b - a) > eps:
            iterations += 1
            lam = (a + b) / 2
            lam1 = lam - delta
            lam2 = lam + delta
            g1 = self.__g(lam1)
            g2 = self.__g(lam2)
            if g1 < g2:  # if need finding max, exchange to '>'
                b = lam
            else:
                a = lam
        lam = (a + b) / 2
        return lam

    def __goldenRatioMethod(self, a, b, eps):
        iterations = 0
        lam1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
        lam2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
        g1 = self.__g(lam1)
        g2 = self.__g(lam2)
        while math.fabs(b - a) > eps:
            iterations += 1
            if g1 < g2:
                b = lam2
                lam2 = lam1
                g2 = g1
                lam1 = a + (3 - math.sqrt(5)) / 2 * (b - a)
                g1 = self.__g(lam1)
            else:
                a = lam1
                lam1 = lam2
                g1 = g2
                lam2 = a + (math.sqrt(5) - 1) / 2 * (b - a)
                g2 = self.__g(lam2)
        lam = (a + b) / 2
        return lam

    def __fibonacciMethod(self, a, b, eps):
        n = math.ceil(math.log2(math.sqrt(5) * (b - a) / eps) / math.log2((1 + math.sqrt(5)) / 2)) - 2
        iterations = 0
        lam1 = a + self.__F(n) / self.__F(n + 2) * (b - 2)
        lam2 = a + self.__F(n + 1) / self.__F(n + 2) * (b - 2)
        g1 = self.__g(lam1)
        g2 = self.__g(lam2)
        k = 1
        while k < n:
            iterations += 1
            if g1 < g2:
                b = lam2
                lam2 = lam1
                g2 = g1
                lam1 = a + self.__F(n - k + 1) / self.__F(n - k + 3) * (b - a)
                g1 = self.__g(lam1)
            else:
                a = lam1
                lam1 = lam2
                g1 = g2
                lam2 = a + self.__F(n - k + 2) / self.__F(n - k + 3) * (b - a)
                g2 = self.__g(lam2)
            k += 1
        lam = (a + b) / 2
        return lam

    def __minFunctionOnLineSearch(self, eps):
        delta = eps / 2
        lam0 = 1

        g0 = self.__g(lam0 - delta)
        g1 = self.__g(lam0)
        g2 = self.__g(lam0 + delta)

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
        g1, g2 = self.__g(lam_next - h), self.__g(lam_next)
        while g1 > g2:
            h *= 2
            lam_next += h
            g1, g2 = g2, self.__g(lam_next)

        if lam_next - h - h / 2 < lam_next:
            return [lam_next - h - h / 2, lam_next]
        else:
            return [lam_next, lam_next - h - h / 2]

    def fastestDescentMethod(self, x1, eps):
        self.x = x1
        s = self.s = self.__grad(x1)

        print("Grad =", s)
        a = self.__minFunctionOnLineSearch(eps)
        b, a = a[1], a[0]
        print("(%s, %s)" % (a, b))
        lam = self.__goldenRatioMethod(a, b, eps)
        print("Lambda =", lam)
        x2 = []
        for i in range(0, len(x1)):
            x2.append(x1[i] + lam * s[i])
        print("Next x =", x2)
        f1 = self.__f(x1)
        f2 = self.__f(x2)
        print("f1 = %s,  f2 = %s" % (f1, f2))
        iterations = 0
        flag = 0
        while math.fabs(f2 - f1) > eps:
            iterations += 1
            x1 = self.x = x2
            f1 = f2
            if flag > 10:
                flag = 0
                x1 = self.x = [1, 1]
                f1 = self.__f(x1)
            s = self.s = self.__grad(x1)

            print("Grad =", s)
            a = self.__minFunctionOnLineSearch(eps)
            b, a = a[1], a[0]
            print("(%s, %s)" % (a, b))
            lam = self.__goldenRatioMethod(a, b, eps)
            print("Lambda =", lam)
            x2 = []
            for i in range(0, len(x1)):
                x2.append(x1[i] + lam * s[i])
            print("Next x =", x2)
            f2 = self.__f(x2)
            print("f1 = %s,  f2 = %s" % (f1, f2))
            if math.fabs(x1[0] - x2[0]) <= eps and math.fabs(x1[1] - x2[1]) <= eps:
                flag += 1
            else:
                flag = 0
            print()

        print(iterations)
        print("f =", self.__f(x2))
        return x2


def main():
    # INITIALIZATION

    x = [100, 100]
    eps = 1e-5
    min = Minimization()
    # min.plotFunction()
    print(min.fastestDescentMethod(x, eps))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
