import numpy as np
import matplotlib.pyplot as plt
from base import NumericalIntegration, Approximation, polynomial


def main():
    integrator = NumericalIntegration('laguerre.txt')

    FUNCTION_LIBRARY = [
        (lambda x: 2 * x + 3, "Liniowa: 2x + 3"),
        (lambda x: np.abs(x), "Wartość bezwzględna: |x|"),
        (lambda x: polynomial(x, [1, 0, -2, 5]), "Wielomian: x³ - 2x + 5"),
        (lambda x: np.sin(x), "Trygonometryczna: sin(x)"),
        (lambda x: np.exp(-x / 3), "Wykładnicza: e^(-x/3)"),
        (lambda x: np.cos(x) ** 2 + np.sin(x), "Złożenie: cos²(x) + sin(x)")
    ]

    print("Dostępne funkcje:")
    for i, (_, desc) in enumerate(FUNCTION_LIBRARY):
        print(f"{i}. {desc}")

    choice = int(input("\nWybierz funkcję (0-5): "))
    func, desc = FUNCTION_LIBRARY[choice]

    print("\nMetody całkowania:")
    method = 'gauss' if int(input("0. Gauss-Laguerre\n1. Simpson\nWybierz (0/1): ")) == 0 else 'simpson'

    params = {}
    if method == 'gauss':
        params['n_points'] = min(max(int(input("Liczba punktów Gaussa (2-10): ")), 2), 10)
    else:
        params['tol'] = max(float(input("Tolerancja (np. 1e-8): ")), 1e-12)

    if int(input("\nTryb:\n0. Stały stopień\n1. Adaptacyjny\nWybierz (0/1): ")):
        target_error = max(float(input("Docelowy błąd (np. 1e-4): ")), 1e-8)
        max_degree = min(int(input("Maksymalny stopień (2-20): ")), 20)

        best_degree = 1
        for degree in range(1, max_degree + 1):
            approx = Approximation(func, degree, integrator, method, params)
            error = approx.calculate_error()
            print(f"Stopień {degree:2d}: błąd = {error:.4e}")

            if error < target_error:
                best_degree = degree
                break
    else:
        user_degree = int(input("Stopień wielomianu (1-15): "))
        best_degree = max(1, min(user_degree, 15))

    approx = Approximation(func, best_degree, integrator, method, params)
    error = approx.calculate_error()

    x = np.linspace(0, 10, 500)
    y_true = func(x)
    y_approx = np.array([approx.evaluate(xi) for xi in x])

    plt.figure(figsize=(12, 7))
    plt.plot(x, y_true, label='Oryginalna', linewidth=2, color='#1f77b4')
    plt.plot(x, y_approx, '--', label=f'Aproksymacja st. {best_degree}', linewidth=2, color='#ff7f0e')

    plt.fill_between(x, y_true, y_approx, color='gray', alpha=0.1)
    plt.title(f"Aproksymacja: {desc}", pad=20, fontsize=14)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='best')

    plt.text(0.95, 0.15, f'Błąd L2: {error:.2e}',
             transform=plt.gca().transAxes,
             ha='right', va='bottom',
             fontsize=12,
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()