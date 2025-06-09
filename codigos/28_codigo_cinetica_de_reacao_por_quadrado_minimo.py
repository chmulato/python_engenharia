import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analisar_cinetica_reacao_minimos_quadrados():
    """
    Simula dados de cinética de reação de primeira ordem, lineariza-os,
    aplica o método dos mínimos quadrados e visualiza os resultados.
    """
    print("--- Exercício de Engenharia Química: Determinação da Constante de Velocidade de Reação ---")

    # --- 1. Simulação de Dados Experimentais (com ruído) ---
    # Parâmetros reais da simulação
    C_A0_real = 10.0  # Concentração inicial real
    k_real = 0.05     # Constante de velocidade real (s^-1)

    # Tempos de amostragem
    tempo = np.arange(0, 101, 5) # De 0 a 100 segundos, a cada 5 segundos

    # Concentração teórica sem ruído
    concentracao_teorica = C_A0_real * np.exp(-k_real * tempo)

    # Adicionar ruído aos dados para simular medições experimentais
    ruido = np.random.normal(0, 0.5, len(tempo)) # Ruído gaussiano com média 0 e desvio padrão 0.5
    concentracao_experimental = concentracao_teorica + ruido
    # Garantir que a concentração não seja negativa devido ao ruído
    concentracao_experimental[concentracao_experimental < 0] = 0.01

    # Criar um DataFrame para os dados
    df_cinetica = pd.DataFrame({
        'Tempo (s)': tempo,
        'Concentração (mol/L)': concentracao_experimental
    })

    print("\n--- Dados Experimentais Simulados (Primeiras 5 linhas) ---")
    print(df_cinetica.head())

    # --- 2. Linearização dos Dados ---
    # Calcular o logaritmo natural da concentração
    # np.log() aplica o logaritmo elemento a elemento
    df_cinetica['ln(Concentração)'] = np.log(df_cinetica['Concentração (mol/L)'])

    print("\n--- Dados Linearizados (Primeiras 5 linhas) ---")
    print(df_cinetica.head())

    # --- 3. Aplicação do Método dos Mínimos Quadrados ---
    # np.polyfit(x, y, grau) ajusta um polinômio (grau 1 para reta)
    # Retorna os coeficientes [m, b] onde m é o coeficiente angular e b é o intercepto
    coeficientes = np.polyfit(df_cinetica['Tempo (s)'], df_cinetica['ln(Concentração)'], 1)
    
    m_ajustado = coeficientes[0] # Coeficiente angular (slope)
    b_ajustado = coeficientes[1] # Coeficiente linear (intercept)

    print(f"\n--- Coeficientes do Ajuste Linear ---")
    print(f"Coeficiente Angular (m): {m_ajustado:.4f}")
    print(f"Coeficiente Linear (b): {b_ajustado:.4f}")

    # --- 4. Determinação da Constante de Velocidade e Concentração Inicial ---
    k_calculado = -m_ajustado
    C_A0_calculado = np.exp(b_ajustado) # np.exp() é a função exponencial

    print(f"\n--- Resultados da Análise Cinética ---")
    print(f"Constante de Velocidade (k): {k_calculado:.4f} s^-1")
    print(f"Concentração Inicial (C_A0): {C_A0_calculado:.4f} mol/L")
    print(f" (Valores reais na simulação: k={k_real}, C_A0={C_A0_real})")

    # --- 5. Visualização dos Resultados ---
    sns.set_style("whitegrid") # Estilo de gráfico do Seaborn

    # Plot 1: Concentração Original vs. Tempo
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1) # 1 linha, 2 colunas, primeiro gráfico
    sns.scatterplot(x='Tempo (s)', y='Concentração (mol/L)', data=df_cinetica, color='blue', label='Dados Experimentais')
    # Plotar a curva teórica ajustada para comparação
    tempo_plot = np.linspace(min(tempo), max(tempo), 100)
    concentracao_ajustada = C_A0_calculado * np.exp(-k_calculado * tempo_plot)
    plt.plot(tempo_plot, concentracao_ajustada, color='red', linestyle='--', label='Curva Ajustada')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Concentração (mol/L)')
    plt.title('Concentração vs. Tempo (Reação de Primeira Ordem)')
    plt.legend()
    plt.grid(True)

    # Plot 2: ln(Concentração) vs. Tempo (Linearizado) com a reta ajustada
    plt.subplot(1, 2, 2) # 1 linha, 2 colunas, segundo gráfico
    sns.scatterplot(x='Tempo (s)', y='ln(Concentração)', data=df_cinetica, color='green', label='Dados Linearizados')
    # Plotar a reta ajustada
    reta_ajustada = m_ajustado * tempo_plot + b_ajustado
    plt.plot(tempo_plot, reta_ajustada, color='orange', linestyle='-', label='Reta de Mínimos Quadrados')
    plt.xlabel('Tempo (s)')
    plt.ylabel('ln(Concentração)')
    plt.title('Linearização e Ajuste por Mínimos Quadrados')
    plt.legend()
    plt.grid(True)

    plt.tight_layout() # Ajusta o layout para evitar sobreposição
    plt.show()

# --- Execução do Exemplo ---
if __name__ == "__main__":
    analisar_cinetica_reacao_minimos_quadrados()
