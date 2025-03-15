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
3. Złożenie dwóch funkcji f(g(x))'''
)
choice = int(input('Wybór: '))
analytical_zeroes = []
match choice:
    case 0:
        func = lambda x: polynomial(x, [1, 1, -2, 0])
        d_func = lambda x: polynomial(x, [3, 2, -2])
        x = numpy.arange(-3, 2, .1)
        analytical_zeroes = [-2, 0 ,1]
    case 1:
        func = lambda x: sin(x) + cos(x)
        d_func = lambda x: cos(x) - sin(x)
        x = numpy.arange(-10, 12, .1)
        analytical_zeroes =[(3/4 * numpy.pi + k * numpy.pi) for k in range(int(x.min()), int(x.max()) + 1)]
    case 2:
        func = lambda x: pow(2, x) - 2
        d_func = lambda x: pow(2, x) * log(2)
        x = numpy.arange(-10, 8, .1)
        analytical_zeroes = [1]
    case 3:
        print("Wybierz funkcję zewnętrzną f: \n0. Wielomian: y = x^3 + x^2 - 2x\n1. Trygonometryczna: y = sin(x) + cos(x)"
              "\n2. Wykładnicza: y = 2^x - 2"
        )
        choice2 = int(input('Wybór: '))
        match choice2:
            case 0:
                f = lambda x: polynomial(x, [1, 1, -2, 0])
                d_f = lambda x: polynomial(x, [3, 2, -2])
            case 1:
                f = lambda x: sin(x) + cos(x)
                d_f = lambda x: cos(x) - sin(x)
            case 2:
                f = lambda x: pow(2, x) - 2
                d_f = lambda x: pow(2, x) * log(2)
        print(
            "Wybierz funkcję wewnętrzną g: \n0. Wielomian: y = x^3 + x^2 - 2x\n1. Trygonometryczna: y = sin(x) + cos(x)"
            "\n2. Wykładnicza: y = 2^x - 2"
        )
        choice3 = int(input('Wybór: '))
        match choice3:
            case 0:
                g = lambda x: polynomial(x, [1, 1, -2, 0])
                d_g = lambda x: polynomial(x, [3, 2, -2])
            case 1:
                g = lambda x: sin(x) + cos(x)
                d_g = lambda x: cos(x) - sin(x)
            case 2:
                g = lambda x: pow(2, x) - 2
                d_g = lambda x: pow(2, x) * log(2)

        func = lambda x: f(g(x))
        d_func = lambda x: d_f(g(x)) * d_g(x)
        x = numpy.arange(-5, 5, .1)
    case _:
        print("Podano błędną wartość!")

#TODO wykres
y = list(map(func, x))

ax = sns.lineplot(x=x, y=y)
sns.scatterplot(x=analytical_zeroes, y=[0] * len(analytical_zeroes), ax=ax, marker="D", edgecolor="green",
                facecolor="None", label="Miejsca zerowe wyznaczone analitycznie")
plt.xlim(x.min(), x.max())
if choice != 3:
    ax.legend(loc='upper left')
plt.grid()
plt.show()


#TODO przedział
a = float(input('Podaj początek przedziału, w którym szukasz miejsca zerowego: ').replace(',', '.'))
b = float(input('Podaj koniec przedziału, w którym szukasz miejsca zerowego: ').replace(',', '.'))

filtered_zeroes = [ zero for zero in analytical_zeroes if a <= zero <= b]

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
#todo osie, analityczne, ticks
ax = sns.lineplot(x=x, y=y)
if(choice != 3):
    sns.scatterplot(x=analytical_zeroes, y=[0] * len(analytical_zeroes), ax=ax, marker="D", edgecolor="green",
                    facecolor="None", label=f"Wynik analityczny: {filtered_zeroes[0]}")
plt.xlim(a, b)
plt.ylim(func(a),func(b))
sns.scatterplot(x=[bisection_result[0]], y=[0], ax=ax, facecolor='None',
                edgecolor='#0000FF', label=f'Wynik bisekcji: {bisection_result[0]}')
sns.scatterplot(x=[newton_results[0]], y=[0], ax=ax, marker='s', facecolor='None',
                edgecolor='#ff0000', label=f'Wynik metody stycznych: {newton_results[0]}')
ax.legend(loc="upper left")
plt.grid()
plt.show()