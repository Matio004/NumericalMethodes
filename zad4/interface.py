from math import sin, cos, pow
from base import *

if __name__ == '__main__':
    print('''Wybierz funkcję:
0. Wielomian: y = x^3 + x^2 - 2x
1. Trygonometryczna: y = sin(x) + cos(x)
2. Wykładnicza: y = 2^x - 2
3. Złożenie funkcji: y = sin(x)^2 + sin(x)''')

    functions = {
        0: lambda x: polynomial(x, [1, 1, -2, 0]),
        1: lambda x: sin(x) + cos(x),
        2: lambda x: pow(2, x) - 2,
        3:  lambda x: polynomial(sin(x), [1, 1, 0]),
    }

    fun = functions.get(int(input()))

    if fun is None:
        exit(1)

    eps = float(input('Podaj dokładność obliczania całki metodą Newtona Cotesa(np. 1e-6): '))

    print('Wynik otrzymany kwadraturą Newtona-Cotesa:', NumericalIntegration().newton_cotes_adaptive(fun, eps))
    print('Wynik otrzymany kwadraturą Gausa:', NumericalIntegration().gauss_quadrature(fun, 3))