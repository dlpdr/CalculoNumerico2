"""Resolve sistemas lineares por eliminacao de Gauss com pivotamento parcial.

O programa primeiro resolve o sistema das tres minas do enunciado e depois
permite informar outros sistemas quadrados de qualquer ordem.
Requer apenas a biblioteca padrao do Python.
"""

from math import isfinite


def resolver_gauss(matriz, termos, tolerancia=1e-12):
    """Resolve A x = b. Retorna x; rejeita matriz singular ou mal condicionada."""
    n = len(matriz)
    if n == 0 or len(termos) != n or any(len(linha) != n for linha in matriz):
        raise ValueError("A matriz deve ser quadrada e ter a mesma ordem do vetor b.")
    if not all(isfinite(float(v)) for linha in matriz for v in linha):
        raise ValueError("A matriz deve conter somente valores numericos finitos.")
    if not all(isfinite(float(v)) for v in termos):
        raise ValueError("O vetor b deve conter somente valores numericos finitos.")

    # Matriz aumentada, em copia para nao modificar os dados fornecidos.
    a = [[float(v) for v in linha] + [float(termos[i])]
         for i, linha in enumerate(matriz)]

    for coluna in range(n):
        pivo_linha = max(range(coluna, n), key=lambda i: abs(a[i][coluna]))
        escala = max(abs(v) for linha in a for v in linha[:-1])
        if escala == 0 or abs(a[pivo_linha][coluna]) <= tolerancia * escala:
            raise ValueError("Sistema singular ou numericamente singular; nao ha solucao unica.")
        a[coluna], a[pivo_linha] = a[pivo_linha], a[coluna]

        for linha in range(coluna + 1, n):
            fator = a[linha][coluna] / a[coluna][coluna]
            a[linha][coluna] = 0.0
            for j in range(coluna + 1, n + 1):
                a[linha][j] -= fator * a[coluna][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        resto = sum(a[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (a[i][n] - resto) / a[i][i]
    return x


def ler_float(mensagem):
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(texto)
            if not isfinite(valor):
                raise ValueError
            return valor
        except ValueError:
            print("Entrada invalida. Informe um numero finito (use ponto ou virgula decimal).")


def ler_sistema():
    while True:
        texto = input("Ordem n da matriz quadrada (inteiro positivo): ").strip()
        try:
            n = int(texto)
            if n > 0:
                break
        except ValueError:
            pass
        print("A ordem deve ser um inteiro positivo.")

    matriz = []
    print(f"Informe os {n} coeficientes de cada linha de A, separados por espaco.")
    for i in range(n):
        while True:
            campos = input(f"Linha {i + 1}: ").replace(",", ".").split()
            try:
                linha = [float(campo) for campo in campos]
                if len(linha) != n or not all(isfinite(v) for v in linha):
                    raise ValueError
                matriz.append(linha)
                break
            except ValueError:
                print(f"Informe exatamente {n} numeros finitos.")

    termos = [ler_float(f"b[{i + 1}]: ") for i in range(n)]
    return matriz, termos


def imprimir_resultado(matriz, termos, solucao, nomes=None):
    print("\nSolucao do sistema:")
    for i, valor in enumerate(solucao):
        nome = nomes[i] if nomes else f"x{i + 1}"
        print(f"  {nome} = {valor:.6f}")
    residuos = [sum(matriz[i][j] * solucao[j] for j in range(len(solucao))) - termos[i]
                for i in range(len(solucao))]
    print("Conferencia (A x - b):", ", ".join(f"{r:.3e}" for r in residuos))


def perguntar_repeticao():
    while True:
        resposta = input("Deseja realizar outro calculo? [S/N]: ").strip().upper()
        if resposta in ("S", "N"):
            return resposta == "S"
        print("Resposta invalida. Digite S para sim ou N para nao.")


def main():
    # Colunas representam as minas; linhas representam os materiais.
    matriz_oficial = [
        [0.55, 0.25, 0.25],  # areia
        [0.30, 0.45, 0.20],  # cascalho fino
        [0.15, 0.30, 0.55],  # cascalho grosso
    ]
    necessidades = [4800.0, 5800.0, 5700.0]
    nomes = ["Volume da Mina 1 (m3)", "Volume da Mina 2 (m3)", "Volume da Mina 3 (m3)"]

    print("=== Necessidades de areia e cascalho: sistema das tres minas ===")
    try:
        solucao = resolver_gauss(matriz_oficial, necessidades)
        imprimir_resultado(matriz_oficial, necessidades, solucao, nomes)
    except ValueError as erro:
        print(f"Nao foi possivel resolver o sistema oficial: {erro}")

    while perguntar_repeticao():
        matriz, termos = ler_sistema()
        try:
            solucao = resolver_gauss(matriz, termos)
            imprimir_resultado(matriz, termos, solucao)
        except ValueError as erro:
            print(f"Nao foi possivel resolver: {erro}")


if __name__ == "__main__":
    main()
