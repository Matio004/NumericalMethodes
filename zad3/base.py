import numpy as np
from math import factorial

def newtonCoefficients(nodes, f_values):
    n = len(nodes)
    h = nodes[1] - nodes[0]

    for i in range(2, n):
        if not np.isclose(nodes[i] - nodes[i - 1], h):
            raise ValueError("Węzły muszą być równoodległe.")

    diff_table = np.zeros((n, n))
    diff_table[:, 0] = f_values

    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = diff_table[i + 1][j - 1] - diff_table[i][j - 1]

    #współczynniki: Δ^i y0 / i!
    a_i = [diff_table[0, i] / factorial(i) for i in range(n)]
    return a_i

def polyHornerValue(x, nodes, coeffs):
    h = nodes[1] - nodes[0]
    x0 = nodes[0]
    t = (x - x0) / h

    n = len(coeffs)
    result = coeffs[-1]
    for i in range(n - 2, -1, -1):
        result = result * (t - i) + coeffs[i]

    return result

def generateEquallySpacedNodes(a, b, n):
    return np.linspace(a, b, n)