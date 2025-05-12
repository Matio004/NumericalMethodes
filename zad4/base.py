import math

import numpy as np
from math import exp, sqrt, pi


class NumericalIntegration:
    def __init__(self):
        # Dla wielomianów Laguerre'a ([0,∞)) z wagą e^(-x)
        self.laguerre_roots = {
            2: np.array([2 - sqrt(2), 2 + sqrt(2)]),
            3: np.array([0.4157745568, 2.2942803603, 6.2899450829]),
            4: np.array([0.3225476896, 1.7457611012, 4.5366202969, 9.3950709123]),
            5: np.array([0.2635603197, 1.4134030591, 3.5964257710, 7.0858100059, 12.6408008443])
        }

        self.laguerre_weights = {
            2: np.array([1 / 2 * (2 + sqrt(2)), 1 / 2 * (2 - sqrt(2))]),
            3: np.array([0.7110930099, 0.2785177336, 0.0103892565]),
            4: np.array([0.6031541043, 0.3574186924, 0.0388879085, 0.0005392947]),
            5: np.array([0.5217556106, 0.3986668110, 0.0759424497, 0.0036117586, 0.0000233700])
        }

    def simpson_rule(self, f, a, b, n):
        """
        Implementacja reguły Simpsona (złożona kwadratura Newtona-Cotesa oparta na trzech węzłach)
        """
        if n % 2 == 1:  # n musi być parzyste
            n += 1

        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = np.array([f(xi) for xi in x])

        result = y[0] + y[-1]
        result += 4 * sum(y[1:-1:2])
        result += 2 * sum(y[2:-2:2])
        result *= h / 3

        return result

    def newton_cotes_adaptive(self, f, tol=1e-6):
        """
        Adaptacyjna złożona kwadratura Newtona-Cotesa dla wariantu 3
        Całkowanie na [0, +∞) z wagą e^(-x)
        """

        # Obliczanie całki na [0, a] i granicy dla [a, +∞)
        return self._compute_boundary_limits_variant3(f, tol)

    def _compute_boundary_limits_variant3(self, f, tol):
        """
        Obliczanie całki na [0, +∞) z wagą e^(-x)
        """
        # Zaczynamy od przedziału [0, 10] i rozszerzamy granicę w razie potrzeby
        a, b = 0, 10
        n = 10
        prev_result = self.simpson_rule(lambda x: f(x) * exp(-x), a, b, n)

        while True:
            n *= 2
            current_result = self.simpson_rule(lambda x: f(x) * exp(-x), a, b, n)
            if abs(current_result - prev_result) < tol:
                result = current_result
                break
            prev_result = current_result

        # Sprawdzamy czy potrzebujemy rozszerzyć granicę
        b_ext = 20
        extension_result = self.simpson_rule(lambda x: f(x) * exp(-x), b, b_ext, n)
        while abs(extension_result) > tol / 10:
            result += extension_result
            b = b_ext
            b_ext = 2 * b
            extension_result = self.simpson_rule(lambda x: f(x) * exp(-x), b, b_ext, n)

        return result

    def gauss_quadrature(self, f, n_points=3):
        """
        Kwadratura Gaussa dla wariantu 3
        Całkowanie na [0, +∞) z wagą e^(-x)
        """
        if n_points not in [2, 3, 4, 5]:
            raise ValueError("Liczba punktów musi być z zakresu 2-5")

        # Dla wielomianów Laguerre'a waga jest już uwzględniona w metodzie
        roots = self.laguerre_roots[n_points]
        weights = self.laguerre_weights[n_points]
        result = sum(weights[i] * f(roots[i]) for i in range(n_points))

        return result


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
