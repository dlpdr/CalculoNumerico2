"""Ponte de Wheatstone resolvida por Gauss-Seidel (sem dependencias externas).

Topologia conforme diagrama do enunciado (nos A, B, C, D):
fonte E entre o no superior A (+) e o no inferior D (0 V);
R1 (A-B) e R4 (B-D) formam o ramo esquerdo;
R2 (A-C) e R3 (C-D) formam o ramo direito;
R5 conecta os nos medios B e C.
"""

from math import isfinite


def gauss_seidel(a, b, epsilon=1e-4, max_iter=10000):
    """Resolve Ax=b; retorna (vetor, iteracoes) ou informa falta de convergencia."""
    n = len(b)
    if n == 0 or len(a) != n or any(len(linha) != n for linha in a):
        raise ValueError("A deve ser quadrada e ter a mesma ordem de b.")
    if not all(isfinite(float(v)) for linha in a for v in linha):
        raise ValueError("A deve conter apenas valores finitos.")
    if not all(isfinite(float(v)) for v in b):
        raise ValueError("b deve conter apenas valores finitos.")
    if epsilon <= 0 or not isfinite(epsilon):
        raise ValueError("epsilon deve ser finito e positivo.")
    if not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("O limite de iteracoes deve ser um inteiro positivo.")
    if any(abs(float(a[i][i])) < 1e-15 for i in range(n)):
        raise ValueError("Gauss-Seidel exige elementos diagonais nao nulos.")

    a = [[float(v) for v in linha] for linha in a]
    b = [float(v) for v in b]
    x = [0.0] * n
    for k in range(1, max_iter + 1):
        anterior = x.copy()
        for i in range(n):
            soma = sum(a[i][j] * x[j] for j in range(i))
            soma += sum(a[i][j] * anterior[j] for j in range(i + 1, n))
            x[i] = (b[i] - soma) / a[i][i]
        if max(abs(x[i] - anterior[i]) for i in range(n)) < epsilon:
            return x, k
    raise RuntimeError(f"Nao convergiu em {max_iter} iteracoes (epsilon={epsilon:g}).")


def montar_sistema(e, r1, r2, r3, r4, r5):
    """Equacoes nodais para as tensoes dos nos medios B (esquerdo) e C (direito)."""
    valores = (e, r1, r2, r3, r4, r5)
    if not all(isfinite(float(v)) for v in valores):
        raise ValueError("Fonte e resistencias devem ser valores finitos.")
    if any(float(r) <= 0 for r in (r1, r2, r3, r4, r5)):
        raise ValueError("Todas as resistencias devem ser positivas.")
    a = [
        [1/r1 + 1/r4 + 1/r5, -1/r5],
        [-1/r5, 1/r2 + 1/r3 + 1/r5],
    ]
    b = [e/r1, e/r2]
    return a, b


def calcular_correntes(e, resistencias, epsilon=1e-4, max_iter=10000):
    r1, r2, r3, r4, r5 = resistencias
    a, b = montar_sistema(e, r1, r2, r3, r4, r5)
    (v_b, v_c), iteracoes = gauss_seidel(a, b, epsilon, max_iter)
    correntes = {
        "I1 (A -> B, em R1)": (e - v_b) / r1,
        "I2 (A -> C, em R2)": (e - v_c) / r2,
        "I3 (C -> D, em R3)": v_c / r3,
        "I4 (B -> D, em R4)": v_b / r4,
        "I5 (B -> C, em R5)": (v_b - v_c) / r5,
    }
    correntes["I6 (corrente total da fonte)"] = (
        correntes["I1 (A -> B, em R1)"] + correntes["I2 (A -> C, em R2)"]
    )
    return (v_b, v_c), correntes, iteracoes


def ler_numero(prompt, positivo=False):
    while True:
        try:
            valor = float(input(prompt).strip().replace(",", "."))
            if not isfinite(valor) or (positivo and valor <= 0):
                raise ValueError
            return valor
        except ValueError:
            criterio = "numero finito positivo" if positivo else "numero finito"
            print(f"Entrada invalida; informe um {criterio}.")


def main():
    print("Ponte de Wheatstone - metodo de Gauss-Seidel")
    epsilon = 1e-4
    max_iter = 10000
    while True:
        print("\n1 - Usar valores do enunciado (E=30 V; R1=20 ohm; R2..R5=120 ohm)")
        print("2 - Informar novos valores")
        opcao = input("Opcao: ").strip()
        if opcao == "1":
            e, resistencias = 30.0, [20.0, 120.0, 120.0, 120.0, 120.0]
        elif opcao == "2":
            e = ler_numero("Fonte E (V): ")
            resistencias = [ler_numero(f"R{i} (ohm): ", positivo=True)
                            for i in range(1, 6)]
            epsilon = ler_numero("Precisao epsilon (ex.: 0.0001): ", positivo=True)
            while True:
                try:
                    max_iter = int(input("Numero maximo de iteracoes: ").strip())
                    if max_iter > 0:
                        break
                except ValueError:
                    pass
                print("Informe um inteiro positivo.")
        else:
            print("Opcao invalida.")
            continue

        try:
            nos, correntes, iteracoes = calcular_correntes(
                e, resistencias, epsilon, max_iter
            )
            print(f"\nTensoes nodais: V_B={nos[0]:.8f} V; V_C={nos[1]:.8f} V")
            print("Correntes (sentidos conforme os nomes):")
            for nome, valor in correntes.items():
                print(f"  {nome}: {valor:.8f} A")
            print("Obs.: No diagrama do PDF, a seta de I1 aponta de B para A; nesse sentido, I1 = -I1(A->B).")
            print(f"Iteracoes para convergir: {iteracoes}")
        except (ValueError, RuntimeError) as erro:
            print(f"Nao foi possivel resolver: {erro}")

        while True:
            repetir = input("Deseja realizar outro calculo? [S/N]: ").strip().upper()
            if repetir in ("S", "N"):
                break
            print("Digite S ou N.")
        if repetir == "N":
            break


if __name__ == "__main__":
    main()
