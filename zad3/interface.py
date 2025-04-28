import matplotlib.pyplot as plt
import numpy as np
import base

functions = {
    'liniowa': lambda x: 2 * x + 1,
    '|x|': lambda x: np.abs(x),
    'wielomian': lambda x: x ** 3 - 2 * x + 1,
    'trygonometryczna': lambda x: np.sin(x) + np.cos(x),
    'złożenie' : base.composition(lambda x: np.abs(x), lambda x: np.cos(x) - 0.5) #|cos(x) - 0.5|
}

def main():
    print("Dostępne funkcje:")
    for idx, func in enumerate(functions.keys()):
        print(f"{idx+1}. {func}")

    choice = int(input("Wybierz funkcję: ")) - 1
    func_name = list(functions.keys())[choice]
    func = functions[func_name]

    a = float(input("Podaj początek przedziału a: "))
    b = float(input("Podaj koniec przedziału b: "))
    n = int(input("Podaj liczbę węzłów: "))

    nodes = base.generateEquallySpacedNodes(a, b, n)
    f_values = func(nodes)

    coeffs = base.newtonCoefficients(nodes, f_values)

    x_plot = np.linspace(a, b, 500)
    y_func = func(x_plot)
    y_interp = [base.polyHornerValue(x, nodes, coeffs) for x in x_plot]

    plt.plot(x_plot, y_func, label='Funkcja oryginalna', color='blue')
    plt.plot(x_plot, y_interp, label='Wielomian interpolacyjny', linestyle='--', color='red')
    plt.scatter(nodes, f_values, color='black', label='Węzły interpolacji')
    plt.legend()
    plt.grid(True)

    plt.savefig("interpolacja.png")
    plt.show()

if __name__ == "__main__":
    main()