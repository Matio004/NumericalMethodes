import numpy

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


x = jordan(numpy.array([
    [3, 3, 1],
    [2, 5, 7],
    [-4, -10, -14]
], dtype=numpy.float64), numpy.array([1, 20, -40], dtype=numpy.float64))
print(x)