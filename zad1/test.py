import numpy

from base import polynomial, bisect, newton

func = lambda x: polynomial(x, [1, 1, -2, 0])
d_func = lambda x: polynomial(x, [3, 2, -2])
x = numpy.arange(-3, 2, .1)
a = .6
b = 2
eps = 1e-10
max_iter = None
bisection_result = bisect(func, a, b, eps, max_iter)
newton_results = newton(func, d_func, a, b, eps, max_iter)
print(bisection_result)
print(newton_results)