import re

import numpy
from math import exp, comb, factorial


class NumericalIntegration:
    def __init__(self, filepath):
        self.laguerre_weights = {}
        self.laguerre_roots = {}

        # Dla wielomianów Laguerre'a ([0,∞)) z wagą e^(-x)
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        n = None
        weights = []
        roots = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(r'n\s*=\s*(\d+)', line)
            if match:
                if n is not None:
                    # Zapisz poprzednie dane
                    self.laguerre_weights[n] = numpy.array(weights)
                    self.laguerre_roots[n] = numpy.array(roots)
                    weights = []
                    roots = []
                n = int(match.group(1))
            else:
                parts = line.split()
                if len(parts) >= 2:
                    weight = float(parts[0])
                    root = float(parts[1])
                    weights.append(weight)
                    roots.append(root)

        # Zapisz dane dla ostatniego n
        if n is not None and weights and roots:
            self.laguerre_weights[n] = numpy.array(weights)
            self.laguerre_roots[n] = numpy.array(roots)

    def simpson_rule(self, f, a, b, n):
        """
        Implementacja reguły Simpsona (złożona kwadratura Newtona-Cotesa oparta na trzech węzłach)
        """
        if n % 2 == 1:  # n musi być parzyste
            n += 1

        h = (b - a) / n
        x = numpy.linspace(a, b, n + 1)
        y = numpy.array([f(xi) for xi in x])

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


def poly_add(p1, p2):
    max_len = max(len(p1), len(p2))
    p1 += [0] * (max_len - len(p1))
    p2 += [0] * (max_len - len(p2))
    return [a + b for a, b in zip(p1, p2)]


def poly_sub(p1, p2):
    max_len = max(len(p1), len(p2))
    p1 += [0] * (max_len - len(p1))
    p2 += [0] * (max_len - len(p2))
    return [a - b for a, b in zip(p1, p2)]


def poly_mul_scalar(p, scalar):
    return [coef * scalar for coef in p]


def poly_mul_x(p):
    return [0] + p


def laguerre_coeffs(n):

    L0 = [1]  # L_0(x) = 1
    if n == 0:
        return L0
    L1 = [-1, 1]  # L_1(x) = x - 1
    if n == 1:
        return L1

    for k in range(1, n):
        # (x - 2k - 1) * Lk = x * Lk - (2k + 1) * Lk
        xLk = poly_mul_x(L1)
        term1 = poly_sub(xLk, poly_mul_scalar(L1, 2 * k + 1))
        term2 = poly_mul_scalar(L0, k * k)
        L2 = poly_sub(term1, term2)
        L0, L1 = L1, L2

    return L1

class Approximation:
    def __init__(self, func, degree, integrator, method='gauss', params=None):
        self.func = func
        self.degree = degree
        self.integrator = integrator
        self.method = method
        self.params = params or {}
        self.coeffs = []
        self.laguerre_poly = []
        self._init_polynomials()
        self._calculate_coefficients()

    def _init_polynomials(self):
        for n in range(self.degree + 1):
            self.laguerre_poly.append(laguerre_coeffs(n))

    def _calculate_coefficients(self):
        global integral
        self.coeffs = []
        for k in range(self.degree + 1):
            Lk = self.laguerre_poly[k]

            def integrand(x):
                return self.func(x) * polynomial(x, Lk)

            if self.method == 'gauss':
                integral = self.integrator.gauss_quadrature(
                    integrand,
                    self.params.get('n_points', 5)
                )
            elif self.method == 'simpson':
                integral = self.integrator.newton_cotes_adaptive(integrand,
                    self.params.get('tol', 1e-8)
                )

            norm = factorial(k) ** 2
            self.coeffs.append(integral / norm)

    def evaluate(self, x):
        result = 0.0
        for k in range(self.degree + 1):
            result += self.coeffs[k] * polynomial(x, self.laguerre_poly[k])
        return result

    def calculate_error(self):
        if self.method == 'gauss':
            integral = self.integrator.gauss_quadrature(
                lambda x: (self.func(x) - self.evaluate(x)) ** 2,
                self.params.get('n_points', 5)
            )
        else:
            integral = self.integrator.newton_cotes_adaptive(
                lambda x: (self.func(x) - self.evaluate(x)) ** 2,
                self.params.get('tol', 1e-8))

        return numpy.sqrt(abs(integral))
