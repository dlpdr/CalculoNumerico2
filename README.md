# Atividade Complementar de Cálculo Numérico — UNIVASF (2026.2)

Repositório com os códigos em Python referentes às quatro questões sorteadas para a equipe (**01.3**, **02.1**, **03.3** e **04.1**) e o relatório técnico em PDF.

## Integrantes da Equipe
- Marcos Anderson Pereira de Carvalho
- Pedro de Souza Torres
- Rafaela Nunes Albuquerque

**Docente:** Prof. Jorge Luis Cavalcanti Ramos  
**Curso:** Engenharia de Computação — Universidade Federal do Vale do São Francisco (UNIVASF)

---

## Estrutura dos Códigos e Funcionamento

Todos os programas executam inicialmente com os dados oficiais do enunciado, exibem os resultados com clareza, validam as condições matemáticas/numéricas exigidas por cada método e oferecem ao usuário a opção de **inserir novos dados** para resolver problemas semelhantes ou **encerrar a execução**.

### 1. Questão 01.3 — `solucao_minas.py` (Métodos Diretos)
- **Objetivo:** Determinar o volume (em m³) a ser extraído de três minas para atender às demandas de areia, cascalho fino e cascalho grosso.
- **Como funciona:**
  - Modela o problema na forma matricial `A·x = b`, onde cada coluna representa uma mina e cada linha representa um material.
  - Implementa `resolver_gauss(matriz, termos)` utilizando **Eliminação de Gauss com pivotamento parcial** e substituição regressiva.
  - Valida se a matriz é quadrada, contém apenas valores finitos e rejeita sistemas singulares ou numericamente singulares.
  - Exibe a solução e os resíduos de conferência (`A·x - b`).
  - Permite ao usuário informar novos sistemas lineares quadrados de qualquer ordem `n >= 1`.
- **Dependências:** apenas biblioteca padrão do Python (`math`).

### 2. Questão 02.1 — `solucao_wheatstone.py` (Métodos Iterativos)
- **Objetivo:** Calcular as correntes elétricas (`I1` a `I6`) em uma Ponte de Wheatstone usando o **Método Iterativo de Gauss-Seidel**.
- **Como funciona:**
  - Segue exatamente a topologia do diagrama do enunciado (nós `A`, `B`, `C`, `D`): fonte `E` entre `A` (`+`) e `D` (`0 V`); ramo esquerdo com `R1` (`A–B`) e `R4` (`B–D`); ramo direito com `R2` (`A–C`) e `R3` (`C–D`); e resistor central `R5` (`B–C`).
  - A função `montar_sistema` aplica a Lei dos Nós de Kirchhoff em `B` e `C` para montar o sistema 2×2 nas tensões nodais `V_B` e `V_C`.
  - A função `gauss_seidel` resolve o sistema iterativamente até atingir `max |x_i^(k+1) - x_i^(k)| < epsilon` (padrão `epsilon = 0,0001`).
  - A função `calcular_correntes` obtém todas as correntes da ponte (`I1`, `I2`, `I3`, `I4`, `I5`, `I6`) a partir das tensões nodais e informa o número de iterações necessárias.
  - Permite escolher entre os valores do enunciado (`E = 30 V`, `R1 = 20 Ω`, `R2 = R3 = R4 = R5 = 120 Ω`) ou informar novos valores de fonte, resistências, precisão e limite de iterações.
- **Dependências:** apenas biblioteca padrão do Python (`math`).

### 3. Questão 03.3 — `regressao_minimos_quadrados.py` (Mínimos Quadrados)
- **Objetivo:** Ajustar um conjunto de pontos experimentais `(x, F(x))` por uma **reta**, uma **parábola** e uma **função exponencial**, calculando o erro quadrático cometido em cada ajuste.
- **Como funciona:**
  - `ajustar_modelos(x, y)` resolve os problemas de mínimos quadrados com `numpy.linalg.lstsq`:
    - **Reta:** `G(x) = a0 + a1·x`
    - **Parábola:** `G(x) = a0 + a1·x + a2·x²`
    - **Exponencial:** `G(x) = a·e^(b·x)`, obtida pela linearização `ln F(x) = ln(a) + b·x`
  - Calcula o erro quadrático na escala original: `Σ [F(x_i) - G(x_i)]²`.
  - Permite visualizar o gráfico comparativo dos três ajustes (opcional, via Matplotlib) e inserir novos vetores de entrada `(X, F(X))`.
- **Dependências:** `numpy` (obrigatório) e `matplotlib` (opcional, apenas para exibição do gráfico).

### 4. Questão 04.1 — `integracao_secao_rio.py` (Integração Numérica)
- **Objetivo:** Calcular a área da seção transversal de um rio a partir de profundidades medidas em pontos discretos igualmente espaçados (`h = 2 m`).
- **Como funciona:**
  - `trapezio_repetido(x, y)` calcula a integral pela **Regra do Trapézio Repetida** (suportando inclusive espaçamentos não uniformes).
  - `simpson_13_repetido(x, y)` calcula a integral pela **Regra de Simpson 1/3 Repetida**, validando previamente que o passo `h` é uniforme e que o número de subintervalos `n` é par.
  - `exibir_comparacao(x, y)` apresenta as duas estimativas de área e a diferença absoluta entre elas.
  - Permite ao usuário informar novas listas de posições `x` e profundidades `y` para calcular outras seções transversais.
- **Dependências:** apenas biblioteca padrão do Python (`math`).

---

## Como Executar

Certifique-se de ter o Python 3 instalado. Caso utilize a regressão ou gráficos, instale as dependências:

```bash
python -m pip install numpy matplotlib
```

Execute cada programa diretamente no terminal:

```bash
python solucao_minas.py
python solucao_wheatstone.py
python regressao_minimos_quadrados.py
python integracao_secao_rio.py
```
