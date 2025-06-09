import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calibrar_sensor_pressao(nome_arquivo, grau_polinomio=1):
    """
    Realiza a calibração de um sensor de pressão.

    Args:
        nome_arquivo (str): Nome do arquivo CSV com os dados de calibração.
        grau_polinomio (int, opcional): Grau do polinômio para o ajuste. Padrão é 1 (linear).

    Returns:
        tuple: (coeficientes, equação_curva) ou (None, None) em caso de erro.
    """

    try:
        # 1. Leitura dos Dados
        df = pd.read_csv(nome_arquivo)
        saida_sensor = df['Saida_Sensor']
        pressao_referencia = df['Pressao_Referencia']

        # 2. Ajuste da Curva
        # polyfit retorna os coeficientes do polinômio, do maior grau para o menor
        coeficientes = np.polyfit(saida_sensor, pressao_referencia, grau_polinomio)

        # 3. Equação da Curva
        equacao_curva = "Pressao = "
        for i, coef in enumerate(coeficientes):
            if grau_polinomio - i > 1:
                equacao_curva += f"{coef:.4f} * Saida^{grau_polinomio - i} + "
            elif grau_polinomio - i == 1:
                equacao_curva += f"{coef:.4f} * Saida + "
            else:
                equacao_curva += f"{coef:.4f}"

        # Remover o último " + "
        if equacao_curva.endswith(" + "):
            equacao_curva = equacao_curva[:-3]

        return coeficientes, equacao_curva

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado. Verifique o caminho e o nome do arquivo.")
        return None, None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None, None


def corrigir_medicao(saida_sensor, coeficientes):
    """
    Corrige a medição do sensor usando a equação de calibração.

    Args:
        saida_sensor (float): Saída do sensor (em Volts).
        coeficientes (array_like): Coeficientes do polinômio (retornados por polyfit).

    Returns:
        float: Pressão corrigida (em kPa).
    """

    pressao_corrigida = np.polyval(coeficientes, saida_sensor)
    return pressao_corrigida


def visualizar_calibracao(saida_sensor, pressao_referencia, coeficientes, equacao_curva):
    """
    Plota os dados de calibração e a curva ajustada.

    Args:
        saida_sensor (array_like): Saídas do sensor.
        pressao_referencia (array_like): Pressões de referência.
        coeficientes (array_like): Coeficientes do polinômio.
        equacao_curva (str): Equação da curva.
    """

    plt.figure(figsize=(8, 6))
    plt.plot(saida_sensor, pressao_referencia, 'bo', label='Dados de Calibração')  # 'bo' para pontos azuis
    
    # Gera pontos para a curva ajustada
    saida_sensor_curva = np.linspace(saida_sensor.min(), saida_sensor.max(), 100)
    pressao_curva = np.polyval(coeficientes, saida_sensor_curva)
    plt.plot(saida_sensor_curva, pressao_curva, 'r-', label=f'Ajuste Polinomial ({equacao_curva})')  # 'r-' para linha vermelha

    plt.xlabel('Saída do Sensor (V)')
    plt.ylabel('Pressão (kPa)')
    plt.title('Calibração do Sensor de Pressão')
    plt.legend()
    plt.grid(True)
    plt.show()


# --- Programa Principal ---
if __name__ == "__main__":
    nome_do_arquivo = "calibracao_pressao.csv"
    grau_polinomio = 2  # Escolha o grau do polinômio (1, 2 ou 3)

    coeficientes, equacao_curva = calibrar_sensor_pressao("calibracao_pressao.csv", grau_polinomio)

    if coeficientes is not None:
        print("Coeficientes do polinômio:", coeficientes)
        print("Equação da curva de calibração:", equacao_curva)

        # Testar a correção
        saidas_teste = [0.5, 1.1, 1.9]
        print("\n--- Teste de Correção ---")
        for saida in saidas_teste:
            pressao_corrigida = corrigir_medicao(saida, coeficientes)
            print(f"Saída do sensor: {saida:.2f} V, Pressão corrigida: {pressao_corrigida:.2f} kPa")

        # Visualizar a calibração
        df = pd.read_csv(nome_do_arquivo)
        visualizar_calibracao(df['Saida_Sensor'], df['Pressao_Referencia'], coeficientes, equacao_curva)