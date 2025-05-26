import numpy as np
import matplotlib.pyplot as plt
from base import NumericalIntegration, Approximation, polynomial


def main():
    try:
        integrator = NumericalIntegration('laguerre.txt')
    except FileNotFoundError:
        print("BŁĄD: Nie znaleziono pliku 'laguerre.txt' z węzłami i wagami Gauss-Laguerre'a")
        print("Program będzie działał tylko z metodą Simpson'a")
        integrator = None

    FUNCTION_LIBRARY = [
        (lambda x: 2 * x + 3, "Liniowa: 2x + 3"),
        (lambda x: np.abs(x), "Wartość bezwzględna: |x|"),
        (lambda x: polynomial(x, [1, 0, -2, 5]), "Wielomian: x³ - 2x + 5"),
        (lambda x: np.sin(x), "Trygonometryczna: sin(x)"),
        (lambda x: np.exp(-x / 3), "Wykładnicza: e^(-x/3)"),
        (lambda x: np.cos(x) ** 2 + np.sin(x), "Złożenie: cos²(x) + sin(x)"),
        (lambda x: 1 / (1 + x), "Wymierna: 1/(1+x)"),
        (lambda x: np.sqrt(x) * np.exp(-x / 2), "Złożenie: √x * e^(-x/2)")
    ]

    print("\nDostępne funkcje:")
    for i, (_, desc) in enumerate(FUNCTION_LIBRARY):
        print(f"{i:2d}. {desc}")

    while True:
        try:
            choice = int(input(f"\nWybierz funkcję (0-{len(FUNCTION_LIBRARY) - 1}): "))
            if 0 <= choice < len(FUNCTION_LIBRARY):
                break
            print("Nieprawidłowy wybór!")
        except ValueError:
            print("Wprowadź liczbę!")

    func, desc = FUNCTION_LIBRARY[choice]

    print("\nMetody całkowania:")
    print("0. Gauss-Laguerre (szybka, dokładna)")
    print("1. Simpson (wolniejsza, uniwersalna)")

    if integrator is None:
        print("UWAGA: Dostępna tylko metoda Simpson'a")
        method = 'simpson'
    else:
        while True:
            try:
                method_choice = int(input("Wybierz metodę (0/1): "))
                if method_choice == 0:
                    method = 'gauss'
                    break
                elif method_choice == 1:
                    method = 'simpson'
                    break
                print("Wybierz 0 lub 1!")
            except ValueError:
                print("Wprowadź liczbę!")

    params = {}
    if method == 'gauss':
        available_points = list(integrator.laguerre_roots.keys())
        print(f"Dostępne liczby punktów Gaussa: {available_points}")
        while True:
            try:
                n_points = int(input(f"Liczba punktów Gaussa ({min(available_points)}-{max(available_points)}): "))
                if n_points in available_points:
                    params['n_points'] = n_points
                    break
                print("Niedostępna liczba punktów!")
            except ValueError:
                print("Wprowadź liczbę!")
    else:
        while True:
            try:
                tol = float(input("Tolerancja całkowania (np. 1e-8): "))
                if tol > 0:
                    params['tol'] = max(tol, 1e-12)
                    break
                print("Tolerancja musi być dodatnia!")
            except ValueError:
                print("Wprowadź liczbę!")

    print("\nTryb pracy:")
    print("0. Stały stopień wielomianu")
    print("1. Adaptacyjny dobór stopnia")

    while True:
        try:
            mode = int(input("Wybierz tryb (0/1): "))
            if mode in [0, 1]:
                break
            print("Wybierz 0 lub 1!")
        except ValueError:
            print("Wprowadź liczbę!")

    if mode == 1:
        while True:
            try:
                target_error = float(input("Docelowy błąd aproksymacji (np. 1e-4): "))
                if target_error > 0:
                    break
                print("Błąd musi być dodatni!")
            except ValueError:
                print("Wprowadź liczbę!")

        while True:
            try:
                max_degree = int(input("Maksymalny stopień wielomianu (2-25): "))
                if 2 <= max_degree <= 25:
                    break
                print("Stopień musi być między 2 a 25!")
            except ValueError:
                print("Wprowadź liczbę!")

        print(f"\nSzukanie optymalnego stopnia (błąd < {target_error:.2e})...")
        print("-" * 50)

        best_degree = 1
        best_error = float('inf')

        for degree in range(1, max_degree + 1):
            try:
                approx = Approximation(func, degree, integrator, method, params)
                error = approx.calculate_error()

                print(f"Stopień {degree:2d}: błąd = {error:.4e}")

                if error < target_error:
                    best_degree = degree
                    best_error = error
                    print(f"Osiągnięto docelowy błąd przy stopniu {degree}")
                    break

                if error < best_error:
                    best_error = error
                    best_degree = degree

            except Exception as e:
                print(f"Błąd dla stopnia {degree}: {e}")
                continue

        if best_error >= target_error:
            print(f"Nie osiągnięto docelowego błędu. Najlepszy wynik: stopień {best_degree}, błąd {best_error:.4e}")

    else:
        while True:
            try:
                user_degree = int(input("Stopień wielomianu aproksymującego (1-20): "))
                if 1 <= user_degree <= 20:
                    best_degree = user_degree
                    break
                print("Stopień musi być między 1 a 20!")
            except ValueError:
                print("Wprowadź liczbę!")

    print(f"\nObliczanie aproksymacji stopnia {best_degree}...")

    try:
        approx = Approximation(func, best_degree, integrator, method, params)
        error = approx.calculate_error()

        print(f"\nWspółczynniki aproksymacji w bazie Laguerre'a:")
        for k, coeff in enumerate(approx.coeffs):
            print(f"c_{k} = {coeff:12.6e}")

        x = np.linspace(0, 8, 500)
        y_true = np.array([func(xi) for xi in x])
        y_approx = np.array([approx.evaluate(xi) for xi in x])

        plt.figure(figsize=(12, 7))

        plt.plot(x, y_true, label='Funkcja oryginalna', linewidth=2.5, color='#1f77b4')
        plt.plot(x, y_approx, '--', label=f'Aproksymacja (stopień {best_degree})',
                 linewidth=2, color='#ff7f0e')

        plt.fill_between(x, y_true, y_approx, color='red', alpha=0.2, label='Różnica')
        plt.title(f"Aproksymacja wielomianami Laguerre'a: {desc}", fontsize=14, pad=15)
        plt.xlabel('x', fontsize=12)
        plt.ylabel('f(x)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='best', fontsize=11)

        info_text = f'Stopień: {best_degree}\n'
        info_text += f'Błąd L2: {error:.3e}\n'
        info_text += f'Metoda: {"Gauss-Laguerre" if method == "gauss" else "Simpson"}'

        plt.text(0.98, 0.98, info_text,
                 transform=plt.gca().transAxes,
                 ha='right', va='top',
                 fontsize=11,
                 bbox=dict(facecolor='white', edgecolor='gray', alpha=0.9, pad=8))

        plt.tight_layout()
        plt.show()

        print(f"\nPodsumowanie:")
        print(f"Funkcja: {desc}")
        print(f"Stopień aproksymacji: {best_degree}")
        print(f"Błąd L2: {error:.6e}")
        print(f"Metoda całkowania: {'Gauss-Laguerre' if method == 'gauss' else 'Simpson adaptacyjny'}")

    except Exception as e:
        print(f"Błąd podczas obliczania aproksymacji: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()