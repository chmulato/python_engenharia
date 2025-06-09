import math

def calcular_constante_velocidade(tempos, concentrações):
    """
    Calcula a constante de velocidade de uma reação de primeira ordem usando regressão linear.

    Args:
        tempos (list): Lista de tempos (em minutos).
        concentrações (list): Lista de concentrações correspondentes.

    Returns:
        float: Constante de velocidade da reação (k).
    """
    ln_concentrações = [math.log(c) for c in concentrações] # List Comprehension
    n = len(tempos)
    soma_t = sum(tempos)
    soma_lnc = sum(ln_concentrações)
    soma_t_lnc = sum(tempos[i] * ln_concentrações[i] for i in range(n))
    soma_t_quadrado = sum(t**2 for t in tempos)

    numerador = n * soma_t_lnc - soma_t * soma_lnc
    denominador = n * soma_t_quadrado - soma_t**2

    if denominador == 0:
        return 0  # Evitar divisão por zero
    else:
        inclinacao = numerador / denominador
        k = -inclinacao
        return k

def gerar_grafico_texto(x_dados, y_dados, x_label, y_label):
    """
    Gera uma representação textual aproximada de um gráfico.

    Args:
        x_dados (list): Lista de valores para o eixo x.
        y_dados (list): Lista de valores para o eixo y.
        x_label (str): Rótulo para o eixo x.
        y_label (str): Rótulo para o eixo y.

    Returns:
        str: Representação textual do gráfico.
    """
    min_x = min(x_dados)
    max_x = max(x_dados)
    min_y = min(y_dados)
    max_y = max(y_dados)

    largura = 50
    altura = 20

    x_intervalo = (max_x - min_x) / largura
    y_intervalo = (max_y - min_y) / altura

    matriz_grafico = [[' ' for _ in range(largura + 1)] for _ in range(altura + 1)]

    # Marcar os pontos
    for i in range(len(x_dados)):
        x_pos = int((x_dados[i] - min_x) / x_intervalo)
        y_pos = altura - int((y_dados[i] - min_y) / y_intervalo)
        if 0 <= x_pos <= largura and 0 <= y_pos <= altura:
            matriz_grafico[y_pos][x_pos] = '*'

    # Eixos
    for i in range(altura + 1):
        matriz_grafico[i][0] = '|'
    for j in range(largura + 1):
        matriz_grafico[altura][j] = '-'

    # Rótulos (simplificado)
    matriz_grafico[0][largura] = y_label[0]  # Primeira letra do rótulo y
    matriz_grafico[altura][largura] = x_label[0]  # Primeira letra do rótulo x

    grafico_texto = "\n".join(["".join(linha) for linha in matriz_grafico])
    return grafico_texto

# 1. Dados Experimentais
tempos = [0, 5, 10, 15, 20, 25, 30]  # minutos
concentrações = [1.6, 1.2, 0.9, 0.6, 0.45, 0.34, 0.25]  # mol/L
temperaturas = [50.0, 52.5, 54.8, 57.1, 59.2, 61.1, 62.8]  # °C

# 2. Calcular a Constante de Velocidade
k = calcular_constante_velocidade(tempos, concentrações)

# 3. Gerar Gráficos (Texto)
grafico_concentração = gerar_grafico_texto(tempos, concentrações, "Tempo (min)", "Concentração (mol/L)")
grafico_temperatura = gerar_grafico_texto(tempos, temperaturas, "Tempo (min)", "Temperatura (°C)")

# 4. Saída de Dados
print("Análise de Reator Químico Batch\n")
print(f"Constante de Velocidade (k): {k:.4f} min^-1\n")

print("Gráfico: Concentração vs. Tempo\n")
print(grafico_concentração)

print("\nGráfico: Temperatura vs. Tempo\n")
print(grafico_temperatura)