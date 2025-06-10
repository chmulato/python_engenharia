import numpy as np
import pandas as pd # Para apresentação tabular dos resultados

def analisar_rede_processos():
    """
    Realiza balanços de massa em uma rede de processos (misturador e separador)
    para determinar vazões e composições desconhecidas.
    """
    print("--- 10.3. Balanço de Massa e Energia com Dados Reais ou Simulados ---")
    print("\n--- Exemplo: Balanço de Massa em uma Rede de Processos ---")

    # --- 1. Dados de Entrada (Simulados) ---
    # Corrente 1
    m1 = 100.0  # kg/h
    xA1 = 0.7   # fração mássica de A

    # Corrente 2
    m2 = 50.0   # kg/h
    xA2 = 0.2   # fração mássica de A

    # Corrente 4 (saída do separador)
    xA4 = 0.95  # fração mássica de A

    # Corrente 5 (saída do separador)
    xA5 = 0.1   # fração mássica de A

    print("\n--- Dados de Entrada ---")
    print(f"Corrente 1: m={m1} kg/h, xA={xA1}")
    print(f"Corrente 2: m={m2} kg/h, xA={xA2}")
    print(f"Corrente 4 (saída separador): xA={xA4}")
    print(f"Corrente 5 (saída separador): xA={xA5}")

    # --- 2. Balanços para o Misturador (Unidade 1) ---
    print("\n--- Balanços para o Misturador ---")
    # Balanço de Massa Total no Misturador
    m3 = m1 + m2
    print(f"Vazão da Corrente 3 (saída do misturador): m3 = {m3:.2f} kg/h")

    # Balanço de Massa para Componente A no Misturador
    # m1*xA1 + m2*xA2 = m3*xA3
    xA3 = (m1 * xA1 + m2 * xA2) / m3
    print(f"Fração mássica de A na Corrente 3: xA3 = {xA3:.4f}")

    # --- 3. Balanços para o Separador (Unidade 2) ---
    print("\n--- Balanços para o Separador ---")
    # Agora, m3 e xA3 são as entradas conhecidas para o separador.
    # As incógnitas são m4 e m5.

    # Equação 1: Balanço de Massa Total no Separador
    # m3 = m4 + m5  =>  1*m4 + 1*m5 = m3
    
    # Equação 2: Balanço de Massa para Componente A no Separador
    # m3*xA3 = m4*xA4 + m5*xA5  =>  xA4*m4 + xA5*m5 = m3*xA3

    # Definir a matriz de coeficientes (A) para o sistema linear [m4, m5]
    matriz_A = np.array([
        [1, 1],          # Coeficientes para m4 e m5 na Eq. 1
        [xA4, xA5]       # Coeficientes para m4 e m5 na Eq. 2
    ])

    # Definir o vetor de termos independentes (B)
    vetor_B = np.array([m3, m3 * xA3])

    print("\nMatriz A (coeficientes para m4, m5):")
    print(matriz_A)
    print("\nVetor B (termos independentes):")
    print(vetor_B)

    # Resolver o sistema de equações lineares Ax = B
    try:
        solucao_m4_m5 = np.linalg.solve(matriz_A, vetor_B)

        m4 = solucao_m4_m5[0]
        m5 = solucao_m4_m5[1]

        print("\n--- Resultados Calculados para o Separador ---")
        print(f"Vazão da Corrente 4: m4 = {m4:.2f} kg/h")
        print(f"Vazão da Corrente 5: m5 = {m5:.2f} kg/h")

        # --- Verificação dos Balanços (Opcional) ---
        print("\n--- Verificação dos Balanços ---")
        print(f"Verificação Total: m4 + m5 = {m4 + m5:.2f} (Esperado: {m3:.2f})")
        print(f"Verificação Componente A: m4*xA4 + m5*xA5 = {m4*xA4 + m5*xA5:.2f} (Esperado: {m3*xA3:.2f})")

    except np.linalg.LinAlgError:
        print("\nErro: A matriz de coeficientes é singular. O sistema não tem solução única.")
        m4 = m5 = np.nan
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        m4 = m5 = np.nan

    # --- Apresentação Final dos Resultados (usando Pandas) ---
    print("\n--- Resumo das Vazões e Composições ---")
    dados_resumo = {
        'Corrente': ['1', '2', '3', '4', '5'],
        'Vazão Mássica (kg/h)': [m1, m2, m3, m4, m5],
        'Fração Mássica A': [xA1, xA2, xA3, xA4, xA5]
    }
    df_resumo = pd.DataFrame(dados_resumo)
    print(df_resumo.round(4).to_string(index=False)) #.to_string(index=False) para não mostrar o índice do DataFrame

# --- Execução do Exemplo ---
if __name__ == "__main__":
    analisar_rede_processos()