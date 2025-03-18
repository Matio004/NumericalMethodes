import math

import matplotlib.pyplot as plt
import numpy
import seaborn as sns

from math import sin, cos, pow, log
from base import polynomial, bisect, newton

print(
'''Wybierz funkcję:
0. Wielomian: y = x^3 + x^2 - 2x
1. Trygonometryczna: y = sin(x) + cos(x)
2. Wykładnicza: y = 2^x - 2
3. Złożenie funkcji: y = sin(x)^2 + sin(x)'''
)
choice = int(input('Wybór: '))
match choice:
    case 0:
        func = lambda x: polynomial(x, [1, 1, -2, 0])
        d_func = lambda x: polynomial(x, [3, 2, -2])
        x = numpy.arange(-3, 2, .1)
    case 1:
        func = lambda x: sin(x) + cos(x)
        d_func = lambda x: cos(x) - sin(x)
        x = numpy.arange(-2*math.pi, 2*math.pi, .1)
    case 2:
        func = lambda x: pow(2, x) - 2
        d_func = lambda x: pow(2, x) * log(2)
        x = numpy.arange(-2.5, 5, .1)
    case 3:
        func = lambda x: polynomial(sin(x), [1, 1, 0])
        d_func = lambda x: (2*sin(x) + 1) * cos(x)
        x = numpy.arange(-6, 8, .1)
    case _:
        pass

y = list(map(func, x))

figure, axes = plt.subplots(1, 1)
sns.lineplot(x=x, y=y, ax=axes)
plt.grid(True)
figure.savefig('funkcja.png')


a = float(input('Podaj początek przedziału, w którym szukasz miejsca zerowego: ').replace(',', '.'))
b = float(input('Podaj koniec przedziału, w którym szukasz miejsca zerowego: ').replace(',', '.'))

stop = int(input('0. Epsilon\n1. Liczba iteracji\nWybór: '))

eps = max_iter = None

match stop:
    case 0:
        eps = float(input('Podaj epsilon: ').replace(',', '.'))
    case 1:
        max_iter = int(input('Podaj liczbę iteracji: '))

try:
    bisection_result = bisect(func, a, b, eps, max_iter)
    newton_results = newton(func, d_func, a, b, eps, max_iter)

    print('Bisekcja:\nMiejsce zerowe: {}; Liczba iteracji: {}; Dokładność: {}'.format(*bisection_result))
    print('Metoda stycznych:\nMiejsce zerowe: {}; Liczba iteracji: {}; Dokładność: {}'.format(*newton_results))

    figure, axes = plt.subplots(1, 1)
    ax = sns.lineplot(x=x, y=y, ax=axes)
    sns.scatterplot(x=[bisection_result[0]], y=[0], ax=ax, facecolor='None',
                    edgecolor='#0000FF', label=f'Wynik bisekcji: {bisection_result[0]}')
    sns.scatterplot(x=[newton_results[0]], y=[0], ax=ax, marker='s', facecolor='None',
                    edgecolor='#ff0000', label=f'Wynik metody stycznych: {newton_results[0]}')
    plt.grid(True)
    ax.legend(loc='upper left')
    figure.savefig('miejsca_zerowe.png')
except ValueError:
    print('Nie można wyznaczyć przybliżonych wartości miejsca zerowego, '
          'brak przeciwnych znaków funkcji na krańcach przedziału')