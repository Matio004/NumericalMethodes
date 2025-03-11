from os.path import split
from math import *

from base import *

print(
'''Wybierz funkcję:
0. Wielomian 2x^5-4x^4+3x^3-6x^2+5x+1
1. Trygonometryczna
2. Wykładnicza 
3. Złożenie funkcji'''
)
choice = int(input('Wybór: '))
match choice:
    case 0:
        func = polynomial(x, [5,-6.5,3,-6,-10, -22])
    case 1:
        func = lambda x: sin(x) + cos(x)
    case 2:
        func = lambda x: exponential(x, 2) - 2
    case 3:
        func = lambda x: sin(polynomial(x, [5, -6.5, 3, -6, -10, -22]))
    case _:
        pass
epsilon = float(input("Podaj żądaną dokładność: "))
bisection=bisect(lambda x: func,-1,3, eps=epsilon)
#TODO wykres
#TODO przedział
#TODO rysunek rozw.