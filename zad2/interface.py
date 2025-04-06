from base import solution
import os
import numpy as np

def display_files():
    try:
        files = [f for f in os.listdir("układy") if f.endswith(".txt")]
        print("Dostępne pliki:")
        for f in files:
            print(f"{f}")
    except FileNotFoundError:
        print("Brak katalogu 'układy'!")

def read_equations(filename: str, n: int):
    try:
        with open(filename, "r") as file:
            matrix = []
            b = []
            for line in file.readlines()[:n]:
                values = list(map(float, line.strip().split()))
                matrix.append(values[:-1])
                b.append(values[-1])
            return np.array(matrix, dtype=np.float64), np.array(b, dtype=np.float64)
    except Exception as e:
        print(f"Błąd: {str(e)}")
        return None, None

def main():
    while True:
        print("Menu:")
        print("1. Wyświetl dostępne pliki tekstowe")
        print("2. Rozwiąż układ równań z pliku")
        print("3. Wyjdź")

        choice = input("Wybierz opcję: ")

        match choice:
            case "1":
                display_files()
                continue
            case "2":
                filename = input("Podaj nazwę pliku (bez rozszerzenia .układy): ").strip()
                filename = f"układy/{filename}.układy"

                while True:
                    n = input("Podaj liczbę równań w układzie: ")
                    if not n.isdigit() or int(n) < 1:
                        print("Podaj dodatnią liczbę całkowitą!")
                        continue
                    n = int(n)
                    break

                matrix, b = read_equations(filename, n)
                if matrix is None:
                    continue

                step_by_step = input("Czy wyświetlić szczegółowe kroki rozwiązania? (T/N): ").lower() == 't'
                if step_by_step:
                    identity = np.identity(matrix.shape[0], dtype=np.float64)
                    print(f"=== POCZĄTEK ===")
                    n = matrix.shape[0]
                    combined = np.hstack((matrix, identity, b.reshape(-1, 1)))
                    for row in combined:
                        print("[", end="")
                        print(" ".join(f"{x:7.3f}" for x in row[:n]), end=" | ")
                        print(" ".join(f"{x:7.3f}" for x in row[n:2 * n]), end=" | ")
                        print(f"{row[-1]:7.3f} ]")
                result = solution(matrix, b, step_by_step=step_by_step)
                if result is not None:
                    print("\nRozwiązanie układu:")
                    for i, x in enumerate(result, 1):
                        print(f"x{i} = {x:.4f}")
                continue
            case "3":
                break

            case _:
                print("Nieprawidłowy wybór!")

if __name__ == "__main__":
    main()