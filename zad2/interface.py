import numpy

from base import jordan
import os


if __name__ == "__main__":
    path = './equations.txt'

    count_equations = int(input('Podaj liczbę równać w układzie: '))

    if count_equations > 10:
        print('Maksymalna liczba równań to 10')
        exit(-1)

    if not os.path.exists(path):
        with open(path, 'x') as file:
            file.write('')

    input(f'Wprowadź do pliku equations.txt macierz rozszerzoną reprezentującą układ {count_equations} równań.'
          f'\nNaciśnij ENTER')

    equations = numpy.loadtxt(path, numpy.float64, delimiter=' ')

    print('Układ:', equations, sep='\n')

    if equations.shape[0] != count_equations:
        print('Podano nieprawidłową liczbę równań!')
        exit(-1)
    if equations.shape[1] - 1 != count_equations:
        print('Zła zmiennych w równaniu!')
        exit(-1)

    print('Wynik:', jordan(equations))