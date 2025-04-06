import numpy

def kronecker_capelli(matrix: numpy.ndarray, b: numpy.ndarray):
    n = matrix.shape[0]
    coeff_rank = numpy.linalg.matrix_rank(matrix) #macierz współczynników
    augmented = numpy.hstack((matrix, b.reshape(-1,1))) #macierz rozszerzona [matrix|b]
    aug_rank = numpy.linalg.matrix_rank(augmented)

    if coeff_rank == aug_rank == n:
        return 'oznaczony'
    elif coeff_rank == aug_rank < n:
        return 'nieoznaczony'
    else:
        return 'sprzeczny'

def jordan(matrix: numpy.ndarray, b: numpy.ndarray):
    new_matrix = matrix.copy()
    new_b = b.copy()
    for k in range(len(matrix)):
        if matrix[k][k] != 0:
            new_b[k] = b[k] / matrix[k][k]
            for j in range(k, len(matrix)):
                new_matrix[k][j] = matrix[k][j]/matrix[k][k]
                for i in range(k):
                    new_matrix[i][j] = matrix[i][j] - (matrix[k][j] * matrix[i][k])/matrix[k][k]
                    new_b[i] = b[i] - (b[k]*matrix[i][k])/matrix[k][k]

                for i in range(k + 1, len(matrix)):
                    new_matrix[i][j] = matrix[i][j] - (matrix[k][j] * matrix[i][k]) / matrix[k][k]
                    new_b[i] = b[i] - (b[k] * matrix[i][k]) / matrix[k][k]
        matrix = new_matrix.copy()
        b = new_b.copy()
    if (matrix == numpy.identity(matrix.shape[0])).all():
        return b

def solution(matrix: numpy.ndarray, b: numpy.ndarray):
    status = kronecker_capelli(matrix, b)
    if status != 'oznaczony':
        print(f'Układ jest {status}.')
        return None
    else:
        return jordan(matrix, b)

x = solution(numpy.array([
    [3, 3, 1],
    [2, 5, 7],
    [-4, -10, -14]
], dtype=numpy.float64), numpy.array([1, 20, -20], dtype=numpy.float64))
print(x)