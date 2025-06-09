import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns

def simular_cstr():
    """
    Simula a dinâmica de um Reator Tanque Agitado Contínuo (CSTR)
    com uma reação de primeira ordem e visualiza a concentração ao longo do tempo.
    """
    print("--- 9.3. Simulações de Tanques, Reatores e Processos Dinâmicos ---")
    print("\n--- Exemplo: CSTR com Reação de Primeira Ordem ---")

    # --- 1. Definir os Parâmetros do CSTR e da Reação ---
    V = 100.0     # Volume do reator (L)
    Q = 10.0      # Vazão volumétrica (L/min)
    k = 0.05      # Constante de velocidade da reação (min^-1)

    # --- 2. Definir a Equação Diferencial Ordinária (EDO) para o CSTR ---
    # A função deve receber (y, t, *args)
    # y é a variável de estado (concentração CA)
    # t é a variável independente (tempo)
    # *args são os parâmetros do sistema (V, Q, k, CA_entrada)
    def dCAdt(CA, t, V, Q, k, CA_entrada_func):
        """
        Define a EDO para a variação da concentração de A no CSTR.
        dCA/dt = (Q/V) * (CA_entrada - CA) - k * CA
        CA_entrada_func é uma função que retorna CA_entrada no tempo t.
        """
        CA_entrada = CA_entrada_func(t) # Obter CA_entrada no tempo atual
        return (Q/V) * (CA_entrada - CA) - k * CA

    # --- 3. Definir a Condição Inicial e o Intervalo de Tempo ---
    CA0 = 0.0       # Concentração inicial de A no reator (mol/L)
    tempo_max = 100 # Tempo máximo de simulação (min)
    t = np.linspace(0, tempo_max, 200) # 200 pontos de tempo para a solução

    # Definir a função para a concentração de entrada (CA_entrada)
    # Vamos simular uma mudança de CA_entrada de 1.0 para 5.0 mol/L em t=20 min
    def CA_entrada_funcao(tempo_atual):
        if tempo_atual < 20:
            return 1.0 # Concentração inicial de entrada
        else:
            return 5.0 # Nova concentração de entrada após 20 min

    # --- 4. Resolver a EDO Numericamente usando odeint ---
    # Passamos a função CA_entrada_funcao como um dos argumentos da EDO
    solucao_CA = odeint(dCAdt, CA0, t, args=(V, Q, k, CA_entrada_funcao))

    # odeint retorna um array 2D, extraímos a primeira coluna para a concentração
    concentracoes = solucao_CA[:, 0]

    # --- 5. Visualizar a Curva da Concentração ---
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))

    # Plotar a concentração no reator
    plt.plot(t, concentracoes, label='Concentração de A no Reator', color='blue', linewidth=2)

    # Plotar a concentração de entrada para contextualizar a mudança
    # Criamos um array de CA_entrada correspondente aos tempos de simulação
    CA_entrada_plot = np.array([CA_entrada_funcao(ti) for ti in t])
    plt.plot(t, CA_entrada_plot, label='Concentração de A na Entrada', color='red', linestyle='--', linewidth=1.5)

    plt.xlabel('Tempo (min)')
    plt.ylabel('Concentração de A (mol/L)')
    plt.title('Dinâmica da Concentração de A em um CSTR')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("\n--- Resultados da Simulação ---")
    print(f"Concentração inicial no reator: {CA0:.2f} mol/L")
    print(f"Concentração final no reator (após {tempo_max} min): {concentracoes[-1]:.2f} mol/L")
    # Encontrar o tempo para atingir 95% da nova concentração de regime
    # (assumindo que o regime final é CA_entrada_final / (1 + k*V/Q))
    CA_entrada_final = CA_entrada_funcao(tempo_max)
    CA_regime_final = CA_entrada_final / (1 + k * V / Q)
    print(f"Concentração de regime permanente esperada (após mudança): {CA_regime_final:.2f} mol/L")

# Para rodar a simulação, basta chamar a função:
if __name__ == "__main__":
    simular_cstr()