
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


def bisect(func, a, b, eps = None, max_iter = None):
    if func(a) * func(b) > 0:
        raise ValueError("Brak przeciwnych znaków funkcji na krańcach badanego przedziału")

    steps = 0
    x0 = 0
    while (abs(x0 - (a + b) / 2) > eps) if max_iter is None else max_iter > steps:
        steps += 1
        x0 = (a + b) / 2
        if func(x0) * func(a) < 0:
            b = x0
        elif func(x0) * func(b) < 0:
            a = x0
    return x0, steps, abs(x0 - (a + b) / 2)

def newton(func, derivative, a, b, eps = None, max_iter = None):
    if func(a) * func(b) > 0:
        raise ValueError("Brak przeciwnych znaków funkcji na krańcach badanego przedziału")

    steps = 0
    while (abs(a - b) > eps) if max_iter is None else max_iter > steps:
        steps += 1
        b, a = a - func(a)/derivative(a), b
    return b, steps, abs(b - a)

if __name__ == '__main__':
    print(bisect(lambda x: polynomial(x, [1.,2.,-2.]), -6., -2., 1e-10))
    print(newton(lambda x: polynomial(x, [1.,2.,-2.]), lambda x: polynomial(x, [2.,2.]), -6., -2., .0000000001))
