import matplotlib.pyplot as plt
import numpy
import seaborn as sns

from math import sin, cos, pow, log
from base import polynomial, bisect, newton
#todo Program ma sprawdzać poprawność założenia o przeciwnych znakach funkcji na krańcach badanego przedziału
print(
'''Wybierz funkcję:
0. Wielomian: y = x^3 + x^2 - 2x - 1
1. Trygonometryczna: y = sin(x) + cos(x)
2. Wykładnicza: y = 2^x - 2
3. Złożenie funkcji: y = sin(x)^2 + sin(x)'''
)
choice = int(input('Wybór: '))
match choice:
    case 0:
        func = lambda x: polynomial(x, [1, 1, -2, -1])
        d_func = lambda x: polynomial(x, [3, 2, -2])
        x = numpy.arange(-3, 2, .1)
    case 1:
        func = lambda x: sin(x) + cos(x)
        d_func = lambda x: cos(x) - sin(x)
        x = numpy.arange(-10, 12, .1)
    case 2:
        func = lambda x: pow(2, x) - 2
        d_func = lambda x: pow(2, x) * log(2)
        x = numpy.arange(-10, 8, .1)
    case 3:
        func = lambda x: polynomial(sin(x), [1, 1, 0])
        d_func = lambda x: (2*sin(x) + 1) * cos(x)
        x = numpy.arange(-6, 8, .1)
    case _:
        pass

#TODO wykres
y = list(map(func, x))

plt.plot(x, y)
plt.show()


#TODO przedział
a = int(input('Podaj początek przedziału, w którym szukasz miejsca zerowego: '))
b = int(input('Podaj koniec przedziału, w którym szukasz miejsca zerowego: '))

stop = int(input('0. Epsilon\n1. Liczba iteracji\nWybór: '))

eps = max_iter = None

match stop:
    case 0:
        eps = float(input('Podaj epsilon: ').replace(',', '.'))
    case 1:
        max_iter = int(input('Podaj liczbę iteracji: '))

bisection_result = bisect(func, a, b, eps, max_iter)
newton_results = newton(func, d_func, a, b, eps, max_iter)

print(bisection_result)
print(newton_results)

#TODO rysunek rozw.