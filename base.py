from math import sin

def polynomial(x, args):
    """

    :param x:
    :param args: kolejność współczynników [ax^n, ax^n-1, ..., a]
    :return:
    """
    y = 0

    for i in args:
        y = y*x + i
    return y

def exponential(x, a):
    temp = 1
    for _ in range(x):
        temp *= a
    return temp

def zlozenie(x, functions):
    for func in reversed(functions):
        x = func(x)
    return x


def bisect(func, a, b, eps = None, max_iter = None):
    steps = 0
    while (abs(a - b) > eps) if max_iter is None else max_iter > steps:
        steps += 1
        x0 = (a + b) / 2
        if func(x0) * func(a) < 0:
            b = x0
        elif func(x0) * func(b) < 0:
            a = x0
    return x0, steps

def newton(func, derivative, a, b, eps = None, max_iter = None):
    x_i = a
    x_i1 = b

    steps = 0
    while (abs(x_i1 - x_i) > eps) if max_iter is None else max_iter > steps:
        steps += 1
        x_i1, x_i = x_i - func(x_i)/derivative(x_i), x_i1
    return x_i1, steps

if __name__ == '__main__':
    print(bisect(lambda x: polynomial(x, [1.,2.,-2.]), -6., -2., 1e-10))
    print(newton(lambda x: polynomial(x, [1.,2.,-2.]), lambda x: polynomial(x, [2.,2.]), -6., -2., .0000000001))
