import re
import numpy as np
from math import exp, factorial, gamma


class NumericalIntegration:
    def __init__(self, filepath):
        self.laguerre_weights = {}
        self.laguerre_roots = {}

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
                    self.laguerre_weights[n] = np.array(weights)
                    self.laguerre_roots[n] = np.array(roots)
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

        if n is not None and weights and roots:
            self.laguerre_weights[n] = np.array(weights)
            self.laguerre_roots[n] = np.array(roots)

    def simpson_rule(self, f, a, b, n):
        if n % 2 == 1:
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
        a, b = 0, 5
        n = 20

        prev_result = self.simpson_rule(lambda x: f(x) * exp(-x), a, b, n)

        for _ in range(10):
            n *= 2
            current_result = self.simpson_rule(lambda x: f(x) * exp(-x), a, b, n)
            if abs(current_result - prev_result) < tol:
                break
            prev_result = current_result

        result = current_result

        while b < 50:
            b_ext = min(b + 10, 50)
            extension = self.simpson_rule(lambda x: f(x) * exp(-x), b, b_ext, n // 2)
            if abs(extension) < tol * 0.01:
                break
            result += extension
            b = b_ext

        return result

    def gauss_quadrature(self, f, n_points=5):
        if n_points not in self.laguerre_roots:
            available = list(self.laguerre_roots.keys())
            n_points = min(available, key=lambda x: abs(x - n_points))

        roots = self.laguerre_roots[n_points]
        weights = self.laguerre_weights[n_points]
        result = sum(weights[i] * f(roots[i]) for i in range(n_points))

        return result


def polynomial(x, coeffs):
    if not coeffs:
        return 0.0

    result = coeffs[0]
    for coeff in coeffs[1:]:
        result = result * x + coeff
    return result


def poly_add(p1, p2):
    max_len = max(len(p1), len(p2))
    p1_ext = [0] * (max_len - len(p1)) + p1
    p2_ext = [0] * (max_len - len(p2)) + p2
    return [a + b for a, b in zip(p1_ext, p2_ext)]


def poly_sub(p1, p2):
    max_len = max(len(p1), len(p2))
    p1_ext = [0] * (max_len - len(p1)) + p1
    p2_ext = [0] * (max_len - len(p2)) + p2
    return [a - b for a, b in zip(p1_ext, p2_ext)]


def poly_mul_scalar(p, scalar):
    return [coef * scalar for coef in p]


def poly_mul_x(p):
    return p + [0]


def laguerre_coeffs(n):
    if n == 0:
        return [1]  # L_0(x) = 1
    elif n == 1:
        return [-1, 1]  # L_1(x) = -x + 1 = 1 - x

    # L_0 i L_1
    L_prev_prev = [1]  # L_0
    L_prev = [-1, 1]  # L_1

    for k in range(1, n):
        # (k+1)*L_{k+1}(x) = (2k+1-x)*L_k(x) - k*L_{k-1}(x)

        # (2k+1)*L_k(x)
        term1 = poly_mul_scalar(L_prev, 2 * k + 1)

        # -x*L_k(x)
        term2 = poly_mul_x(L_prev)
        term2 = poly_mul_scalar(term2, -1)

        # (2k+1-x)*L_k(x)
        combined = poly_add(term1, term2)

        # -k*L_{k-1}(x)
        term3 = poly_mul_scalar(L_prev_prev, -k)

        # Całe wyrażenie
        L_current = poly_add(combined, term3)

        # Dzielenie przez (k+1)
        L_current = poly_mul_scalar(L_current, 1.0 / (k + 1))

        # Przesunięcie dla następnej iteracji
        L_prev_prev = L_prev
        L_prev = L_current

    return L_prev


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
        self.laguerre_poly = []
        for n in range(self.degree + 1):
            self.laguerre_poly.append(laguerre_coeffs(n))

    def _calculate_coefficients(self):
        self.coeffs = []

        for k in range(self.degree + 1):
            Lk_coeffs = self.laguerre_poly[k]

            def integrand(x):
                return self.func(x) * polynomial(x, Lk_coeffs)

            # Oblicz <f, L_k>
            if self.method == 'gauss':
                numerator = self.integrator.gauss_quadrature(
                    integrand,
                    self.params.get('n_points', 7)
                )
            else:
                numerator = self.integrator.newton_cotes_adaptive(
                    integrand,
                    self.params.get('tol', 1e-8)
                )

            denominator = factorial(k)

            self.coeffs.append(numerator / denominator)

    def evaluate(self, x):
        result = 0.0
        for k in range(self.degree + 1):
            Lk_value = polynomial(x, self.laguerre_poly[k])
            result += self.coeffs[k] * Lk_value
        return result

    def calculate_error(self):

        def error_integrand(x):
            diff = self.func(x) - self.evaluate(x)
            return diff * diff

        if self.method == 'gauss':
            integral = self.integrator.gauss_quadrature(
                error_integrand,
                self.params.get('n_points', 7)
            )
        else:
            integral = self.integrator.newton_cotes_adaptive(
                error_integrand,
                self.params.get('tol', 1e-8)
            )

        return np.sqrt(abs(integral))

    def get_polynomial_coeffs(self):
        result_poly = [0]

        for k in range(self.degree + 1):
            Lk_coeffs = self.laguerre_poly[k]
            scaled_Lk = poly_mul_scalar(Lk_coeffs, self.coeffs[k])
            result_poly = poly_add(result_poly, scaled_Lk)

        return result_poly