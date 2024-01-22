# Krus Szymon
# D1 Nr 159612

def eliminacja_gaussa(A, b):
    n = len(b)

    for i in range(n):
        max_index = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_index][i]):
                max_index = j

        A[i], A[max_index] = A[max_index], A[i]
        b[i], b[max_index] = b[max_index], b[i]

        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]

    return x


def metoda_jacobiego(A, b, epsilon=1e-10, max_iter=1000):
    n = len(b)
    x = [0] * n

    for k in range(max_iter):
        x_nowy = [0] * n

        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_nowy[i] = (b[i] - suma) / A[i][i]

        if all(abs(x_nowy[i] - x[i]) < epsilon for i in range(n)):
            return x_nowy

        x = x_nowy

    raise ValueError("Metoda Jacobiego nie dziala")


def wczytaj_dane(plik):
    with open(plik, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()

    A = []
    b = []

    for line in lines[1:]:
        coefficients = list(map(float, line.strip().split()))
        A.append(coefficients[:-1])
        b.append(coefficients[-1])

    return A, b


if __name__ == "__main__":
    plik = "test.txt"
    A, b = wczytaj_dane(plik)

    wynik_gauss = eliminacja_gaussa(A, b)

    print("Rozwiazanie ukladu rownan eliminacja Gaussa:")
    for i, val in enumerate(wynik_gauss):
        print(f"x{i + 1} = {val}")

    print("\n")

    wynik_jacobi = metoda_jacobiego(A, b)

    print("Rozwiazanie ukladu rownan metoda Jacobiego:")
    for i, val in enumerate(wynik_jacobi):
        print(f"x{i + 1} = {val}")
