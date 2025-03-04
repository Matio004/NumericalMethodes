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

print(polynomial(1, [2, 1]))