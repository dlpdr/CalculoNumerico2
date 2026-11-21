"""Ajustes de minimos quadrados: reta, parabola e exponencial.

Requer NumPy. Matplotlib e opcional para a visualizacao.
O ajuste exponencial e feito por linearizacao de ln(F) = ln(a) + b*x.
"""

import math

import numpy as np


def ajustar_modelos(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y):
        raise ValueError("X e F(X) devem ser vetores unidimensionais do mesmo tamanho.")
    if len(x) < 3:
        raise ValueError("Informe ao menos 3 pares de dados para ajustar os tres modelos.")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("Os dados devem conter somente valores numericos finitos.")
    if np.unique(x).size < 3:
        raise ValueError("Sao necessarios ao menos 3 valores distintos de X.")
    if np.any(y <= 0):
        raise ValueError("F(X) deve ser estritamente positivo para o ajuste exponencial linearizado.")

    # np.linalg.lstsq encontra a solucao de min ||A*c-y||_2 sem formar A.T @ A.
    coef_reta, *_ = np.linalg.lstsq(np.column_stack((np.ones_like(x), x)), y, rcond=None)
    coef_parabola, *_ = np.linalg.lstsq(
        np.column_stack((np.ones_like(x), x, x**2)), y, rcond=None
    )
    coef_log, *_ = np.linalg.lstsq(
        np.column_stack((np.ones_like(x), x)), np.log(y), rcond=None
    )
    a_exp = float(np.exp(coef_log[0]))
    b_exp = float(coef_log[1])

    predicoes = {
        "reta": coef_reta[0] + coef_reta[1] * x,
        "parabola": coef_parabola[0] + coef_parabola[1] * x + coef_parabola[2] * x**2,
        "exponencial": a_exp * np.exp(b_exp * x),
    }
    erros = {nome: float(np.sum((y - g) ** 2)) for nome, g in predicoes.items()}
    return {
        "reta": tuple(float(c) for c in coef_reta),
        "parabola": tuple(float(c) for c in coef_parabola),
        "exponencial": (a_exp, b_exp),
        "predicoes": predicoes,
        "erros": erros,
    }


def imprimir_resultados(resultado):
    a0, a1 = resultado["reta"]
    print(f"\nReta: G(x) = {a0:.10g} + ({a1:.10g}) x")
    a0, a1, a2 = resultado["parabola"]
    print(f"Parabola: G(x) = {a0:.10g} + ({a1:.10g}) x + ({a2:.10g}) x^2")
    a, b = resultado["exponencial"]
    print(f"Exponencial: G(x) = {a:.10g} * e^(({b:.10g}) x)")
    print("\nErro quadratico na escala original, soma (F(x_i) - G(x_i))^2:")
    for nome in ("reta", "parabola", "exponencial"):
        print(f"  {nome.capitalize()}: {resultado['erros'][nome]:.10g}")
    print("Nota: o ajuste exponencial minimiza os residuos de ln(F); o erro acima")
    print("      e calculado em F, conforme definido, e nao e o criterio otimizado nesse ajuste.")


def mostrar_grafico(x, y, resultado):
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Matplotlib nao esta instalado. Instale com: pip install matplotlib") from exc
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xx = np.linspace(float(np.min(x)), float(np.max(x)), 400)
    a0, a1 = resultado["reta"]
    p0, p1, p2 = resultado["parabola"]
    a, b = resultado["exponencial"]
    plt.scatter(x, y, color="black", label="Dados")
    plt.plot(xx, a0 + a1 * xx, label="Reta")
    plt.plot(xx, p0 + p1 * xx + p2 * xx**2, label="Parabola")
    plt.plot(xx, a * np.exp(b * xx), label="Exponencial")
    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.title("Ajustes por minimos quadrados")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def ler_vetor(nome):
    while True:
        texto = input(f"Informe os valores de {nome}, separados por espaco ou virgula: ")
        try:
            valores = [float(v) for v in texto.replace(",", " ").split()]
            if not valores or not all(math.isfinite(v) for v in valores):
                raise ValueError
            return valores
        except ValueError:
            print("Entrada invalida; informe uma lista de numeros finitos.")


def main():
    x = [0, 1.5, 2.6, 4.2, 6, 8.2, 10, 11.4]
    y = [18, 13, 11, 9, 6, 4, 2, 1]
    print("Ajustes de minimos quadrados para reta, parabola e exponencial")
    while True:
        try:
            resultado = ajustar_modelos(x, y)
            imprimir_resultados(resultado)
            if input("Deseja visualizar o grafico? [S/N]: ").strip().upper() == "S":
                mostrar_grafico(x, y, resultado)
        except (ValueError, RuntimeError) as erro:
            print(f"Nao foi possivel concluir o ajuste: {erro}")

        while True:
            resposta = input("Deseja inserir outro conjunto de dados? [S/N]: ").strip().upper()
            if resposta in ("S", "N"):
                break
            print("Digite S ou N.")
        if resposta == "N":
            return

        while True:
            novos_x = ler_vetor("X")
            novos_y = ler_vetor("F(X)")
            try:
                # Validar antes de substituir os dados em uso.
                ajustar_modelos(novos_x, novos_y)
                x, y = novos_x, novos_y
                break
            except ValueError as erro:
                print(f"Dados invalidos para os tres modelos: {erro}")


if __name__ == "__main__":
    main()
