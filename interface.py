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
        func = None
    case 1:
        func = sin
    case 2:
        func = cos
    case 3:
        func = tan
    case _:
        pass