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

def bisect(func, a, b, eps):
    while abs(a - b) > eps:
        x0 = (a + b) / 2
        if func(x0) * func(a) < 0:
            b = x0
        elif func(x0) * func(b) < 0:
            a = x0
    return x0

def newton(func, derivative, a, b, eps):
    x_i = a
    x_i1 = a

    for i in range(10):
        x_i1, x_i = x_i - func(x_i)/derivative(x_i), x_i1
    return x_i1

print(bisect(lambda x: polynomial(x, [1.,2.,-2.]), -6., -2., 1e-10))
print(newton(lambda x: polynomial(x, [1.,2.,-2.]), lambda x: polynomial(x, [2.,2.]), -6., -2., 1e-10))