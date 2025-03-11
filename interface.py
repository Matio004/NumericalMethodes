from math import *
from base import *

print(
'''Wybierz funkcję:
0. Wielomian y = 5x^4-6.5x^3+3x^2-6x^2-10x - 22
1. Trygonometryczna y = sin(x) + cos(x)
2. Wykładnicza y = e^(x-1) - 2 
3. Złożenie funkcji'''
)
choice = int(input('Wybór: '))
match choice:
    case 0:
        func = polynomial(x, [5,-6.5,3,-6,-10, -22])
    case 1:
        func = sin(x) + cos(x)
    case 2:
        func = exponential(x,exp(x-1))
    case 3:

    case _:
        pass
epsilon = float(input("Podaj żądaną dokładność: "))
bisection=bisect(lambda x: func,-1,3, eps=epsilon)
#TODO wykres
#TODO przedział
#TODO rysunek rozw.