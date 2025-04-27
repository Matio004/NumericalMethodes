from base import newtonCoefficients, polyHornerValue

nodes = [1, 2, 3]
f_values = [2, 10, 2]
coeffs = newtonCoefficients(nodes, f_values)

x = 2.5
result = polyHornerValue(x, nodes, coeffs)
print(f"W({x}) = {result}")