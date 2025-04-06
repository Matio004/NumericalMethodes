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

def jordan(matrix: numpy.ndarray, b: numpy.ndarray, step_by_step=False):
    new_matrix = matrix.copy()
    new_b = b.copy()
    identity = numpy.eye(matrix.shape[0], dtype=numpy.float64)
    for k in range(len(matrix)):
        if matrix[k][k] != 0:
            identity[k] /= new_matrix[k][k]
            new_b[k] = b[k] / matrix[k][k]
            for j in range(k, len(matrix)):
                new_matrix[k][j] = matrix[k][j]/matrix[k][k]
                for i in range(k):
                    identity[i] -= identity[k] * new_matrix[i][k]
                    new_matrix[i][j] = matrix[i][j] - (matrix[k][j] * matrix[i][k])/matrix[k][k]
                    new_b[i] = b[i] - (b[k]*matrix[i][k])/matrix[k][k]

                for i in range(k + 1, len(matrix)):
                    identity[i] -= identity[k] * new_matrix[i][k]
                    new_matrix[i][j] = matrix[i][j] - (matrix[k][j] * matrix[i][k]) / matrix[k][k]
                    new_b[i] = b[i] - (b[k] * matrix[i][k]) / matrix[k][k]
        matrix = new_matrix.copy()
        b = new_b.copy()
        if step_by_step:
            print(f"\n=== KROK {k + 1} ===")
            n= matrix.shape[0]
            combined = numpy.hstack((new_matrix, identity, new_b.reshape(-1, 1)))
            for row in combined:
                print("[", end="")
                print(" ".join(f"{x:7.3f}" for x in row[:n]), end=" | ")
                print(" ".join(f"{x:7.3f}" for x in row[n:2 * n]), end=" | ")
                print(f"{row[-1]:7.3f} ]")
    return b

def solution(matrix: numpy.ndarray, b: numpy.ndarray, step_by_step=False):
    status = kronecker_capelli(matrix, b)
    if status != 'oznaczony':
        print(f'Układ jest {status}.')
        return None
    else:
        return jordan(matrix, b, step_by_step=step_by_step)