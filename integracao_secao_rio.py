"""Area de uma secao transversal por integracao numerica composta."""

import math


def validar_dados(x, y):
    """Valida vetores de mesmo tamanho e posicoes estritamente crescentes."""
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("x e y devem ter o mesmo tamanho e pelo menos dois pontos.")
    if not all(math.isfinite(float(v)) for v in x + y):
        raise ValueError("Todos os dados devem ser numeros finitos.")
    if any(float(x[i + 1]) <= float(x[i]) for i in range(len(x) - 1)):
        raise ValueError("As posicoes x devem estar em ordem estritamente crescente.")
    if any(float(valor) < 0 for valor in y):
        raise ValueError("As profundidades devem ser nao negativas.")


def trapezio_repetido(x, y):
    """Integra dados tabulados pela regra do trapezio, inclusive malha irregular."""
    validar_dados(x, y)
    return sum((x[i + 1] - x[i]) * (y[i] + y[i + 1]) / 2
               for i in range(len(x) - 1))


def simpson_13_repetido(x, y, tolerancia=1e-9):
    """Integra por Simpson 1/3 composto; requer passo uniforme e n par."""
    validar_dados(x, y)
    n = len(x) - 1
    if n % 2 != 0:
        raise ValueError("Simpson 1/3 repetido exige numero par de subintervalos.")
    passos = [x[i + 1] - x[i] for i in range(n)]
    h = passos[0]
    if any(abs(passo - h) > tolerancia * max(1.0, abs(h)) for passo in passos[1:]):
        raise ValueError("Simpson 1/3 repetido exige posicoes igualmente espacadas.")
    soma_impares = sum(y[i] for i in range(1, n, 2))
    soma_pares = sum(y[i] for i in range(2, n, 2))
    return h / 3 * (y[0] + y[-1] + 4 * soma_impares + 2 * soma_pares)


def ler_vetor(rotulo):
    while True:
        try:
            texto = input(f"Informe {rotulo} separados por espaco ou virgula: ")
            valores = [float(item) for item in texto.replace(",", " ").split()]
            if not valores or not all(math.isfinite(v) for v in valores):
                raise ValueError
            return valores
        except ValueError:
            print("Entrada invalida. Informe uma lista de numeros finitos.")


def exibir_comparacao(x, y):
    area_trapezio = trapezio_repetido(x, y)
    print(f"\nRegra do Trapezio Repetida: {area_trapezio:.6f} m^2")
    try:
        area_simpson = simpson_13_repetido(x, y)
        print(f"Regra de Simpson 1/3 Repetida: {area_simpson:.6f} m^2")
        print(f"Diferenca absoluta: {abs(area_trapezio - area_simpson):.6f} m^2")
    except ValueError as erro:
        print(f"Regra de Simpson 1/3 Repetida: indisponivel ({erro})")


def main():
    # Dados do enunciado: 11 ordenadas geram 10 subintervalos de 2 m.
    x = [2.0 * i for i in range(11)]
    y = [0, 1.8, 2, 4, 4, 6, 4, 3.6, 3.4, 2.8, 0]
    print("Area da secao transversal do rio")
    while True:
        try:
            validar_dados(x, y)
            exibir_comparacao(x, y)
        except ValueError as erro:
            print(f"Nao foi possivel calcular: {erro}")

        while True:
            resposta = input("Deseja calcular outra secao? [S/N]: ").strip().upper()
            if resposta in ("S", "N"):
                break
            print("Digite S ou N.")
        if resposta == "N":
            break

        while True:
            x_novo = ler_vetor("as posicoes x (m)")
            y_novo = ler_vetor("as profundidades y (m)")
            try:
                validar_dados(x_novo, y_novo)
                x, y = x_novo, y_novo
                break
            except ValueError as erro:
                print(f"Dados invalidos: {erro}")


if __name__ == "__main__":
    main()
