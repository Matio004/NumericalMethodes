import numpy


def jordan(matrix: numpy.ndarray, b: numpy.ndarray = None):
    if b is not None:
        augmented = numpy.hstack([matrix, b.reshape((-1, 1))])
    else:
        augmented = matrix

    for k in range(matrix.shape[0]):
        if numpy.isclose(augmented[k, k], 0):
            for j in range(k + 1, matrix.shape[0]):
                if not numpy.isclose(augmented[j, k], 0):
                    augmented[[k, j]] = augmented[[j, k]]
                    break
            else:
                if numpy.isclose(augmented[k, -1], 0):
                    return 'nieoznaczony'
                else:
                    return 'sprzeczny'

        augmented[k] /= augmented[k, k]

        for i in range(matrix.shape[0]):
            if i != k:
                augmented[i] -= augmented[i, k] * augmented[k]

    return augmented[:, -1]
