from os.path import split
from math import *

from base import *

print(
'''Wybierz funkcję:
0. Wielomian
1. Trygonometryczna
2. Wykładnicza 
3. Złożenie funkcji'''
)
choice = int(input('Wybór: '))
match choice:
    case 0:
        func =
    case 1:
        func = sin
    case 2:
        func = cos
    case 3:
        func = tan
    case _:
        pass