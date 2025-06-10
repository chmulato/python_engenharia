import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd # Para organizar os resultados da simulação

# --- 1. Definir os Parâmetros do Reator e da Reação (da Tarefa 1) ---
AT = 5.0        # Área da seção transversal do reator (m^2)
H_MAX = 2.0     # Altura máxima do reator (m)
rho = 1000.0    # Densidade do líquido (kg/m^3)
Cp = 4.186      # Capacidade calorífica do líquido (kJ/kg.°C)
Cp_J_kg_C = Cp * 1000 # Convertendo kJ/kg.°C para J/kg.°C

k0 = 1.0e10     # Fator pré-exponencial da constante de velocidade (min^-1)
Ea_R = 8000.0   # Energia de ativação / Constante dos gases (K)
delta_H_reacao = -50000.0 # Entalpia de reação (J/mol) - Negativo para exotérmica

Q_entrada_base_const = 0.1 # Vazão volumétrica de entrada base (m^3/min)
Q_entrada_max = 0.5  # Vazão máxima da bomba de entrada (m^3/min)
T_entrada_const = 25.0     # Temperatura da corrente de entrada (°C)
CA_entrada_const = 1.0     # Concentração do reagente A na entrada (mol/L)

Ao = 0.01       # Área do orifício de saída (m^2)
Cd = 0.6        # Coeficiente de descarga do orifício (adimensional)
g = 9.81 * 60**2 # Aceleração da gravidade (m/min^2)

Q_aquecedor_max = 50000.0 # Potência máxima do aquecedor (J/min)
Q_resfriador_max = -50000.0 # Potência máxima do resfriador (J/min)

# Parâmetros de Controle (Ganhos)
Kp_nivel = 0.5
Kp_temp = 100.0

# --- Funções de Perfil de Setpoint e Distúrbio (NOVIDADE DA TAREFA 4) ---
def setpoint_nivel_profile(t):
    """Define o setpoint de nível em função do tempo."""
    if t < 50:
        return 1.0 # m
    else:
        return 1.5 # m (mudança de setpoint após 50 min)

def setpoint_temperatura_profile(t):
    """Define o setpoint de temperatura em função do tempo."""
    if t < 20:
        return 50.0 # °C
    elif t < 80:
        return 60.0 # °C (mudança de setpoint após 20 min)
    else:
        return 55.0 # °C (outra mudança de setpoint após 80 min)

def Q_entrada_disturbance_profile(t):
    """Simula um distúrbio na vazão de entrada base."""
    if t < 10:
        return Q_entrada_base_const
    elif t < 60:
        return Q_entrada_base_const * 1.2 # Aumento de 20% na vazão de entrada
    else:
        return Q_entrada_base_const # Retorna ao normal

def T_entrada_disturbance_profile(t):
    """Simula um distúrbio na temperatura de entrada."""
    if t < 40:
        return T_entrada_const
    elif t < 70:
        return T_entrada_const + 10.0 # Aumento de 10°C na temperatura de entrada
    else:
        return T_entrada_const

def CA_entrada_disturbance_profile(t):
    """Simula um distúrbio na concentração de entrada."""
    return CA_entrada_const # Mantendo constante para este exemplo

# --- 2. Implementar a função que descreve o sistema de EDOs acopladas (da Tarefa 2 e 3) ---
def reactor_odes(Y, t, params):
    """
    Define o sistema de Equações Diferenciais Ordinárias (EDOs) acopladas
    para o reator químico, incluindo a lógica de controle e perfis de entrada.
    """
    h, T, CA = Y # Desempacotar as variáveis de estado

    # Desempacotar os parâmetros e funções de perfil
    AT, Ao, Cd, g, rho, Cp_J_kg_C, k0, Ea_R, delta_H_reacao, \
    Q_entrada_max, Q_aquecedor_max, Q_resfriador_max, Kp_nivel, Kp_temp, \
    setpoint_nivel_func, setpoint_temperatura_func, \
    Q_entrada_base_func, T_entrada_func, CA_entrada_func = params

    # --- Lógica de Controle e Perfis de Entrada ---
    current_setpoint_nivel = setpoint_nivel_func(t)
    current_setpoint_temperatura = setpoint_temperatura_func(t)
    current_Q_entrada_base = Q_entrada_base_func(t)
    current_T_entrada = T_entrada_func(t)
    current_CA_entrada = CA_entrada_func(t)

    # 1. Controle de Nível (Q_entrada)
    erro_nivel = current_setpoint_nivel - h
    Q_entrada_control = current_Q_entrada_base + Kp_nivel * erro_nivel
    Q_entrada = np.clip(Q_entrada_control, 0.0, Q_entrada_max)

    # 2. Controle de Temperatura (Q_aquecedor)
    erro_temp = current_setpoint_temperatura - T
    Q_aquecedor_control = Kp_temp * erro_temp
    Q_aquecedor = np.clip(Q_aquecedor_control, Q_resfriador_max, Q_aquecedor_max)

    # --- Cálculos Intermediários ---
    if h <= 0: Q_saida = 0.0
    else: Q_saida = Cd * Ao * np.sqrt(2 * g * h)
    
    V_liquido = AT * h
    if V_liquido <= 1e-6: V_liquido = 1e-6 # Evitar divisão por zero

    k_arrhenius = k0 * np.exp(-Ea_R / (current_T_entrada + 273.15)) # k depende da T_entrada para este exemplo
    r_A = k_arrhenius * CA

    Q_reacao = (-delta_H_reacao) * r_A * V_liquido

    # --- EDOs ---
    dhdt = (Q_entrada - Q_saida) / AT

    dCAdt = (Q_entrada * current_CA_entrada - Q_saida * CA - V_liquido * r_A) / V_liquido
    if h <= 0: dCAdt = 0.0

    dTdt = (Q_entrada * (current_T_entrada - T) / V_liquido) + \
           (Q_reacao / (V_liquido * rho * Cp_J_kg_C)) + \
           (Q_aquecedor / (V_liquido * rho * Cp_J_kg_C))
    if h <= 0: dTdt = 0.0

    return dhdt, dTdt, dCAdt

# --- Função Principal de Simulação (NOVIDADE DA TAREFA 4) ---
def simular_sistema_reator():
    """
    Orquestra a simulação completa do reator, incluindo EDOs, controle,
    perfis de setpoint/distúrbio e visualização.
    """
    print("--- 10.4. Simulação Completa do Sistema Reator ---")

    # --- 1. Definir Condições Iniciais e Intervalo de Tempo ---
    h0 = 0.5        # Altura inicial (m)
    T0 = 25.0       # Temperatura inicial (°C)
    CA0 = 0.0       # Concentração inicial de A (mol/L)
    Y0 = np.array([h0, T0, CA0]) # Corrigido

    tempo_max = 150 # Tempo máximo de simulação (min)
    t_span = np.linspace(0, tempo_max, 500) # 500 pontos de tempo para a solução

    # --- 2. Empacotar Parâmetros e Funções de Perfil para a EDO ---
    params = (AT, Ao, Cd, g, rho, Cp_J_kg_C, k0, Ea_R, delta_H_reacao,
              Q_entrada_max, Q_aquecedor_max, Q_resfriador_max, Kp_nivel, Kp_temp,
              setpoint_nivel_profile, setpoint_temperatura_profile,
              Q_entrada_disturbance_profile, T_entrada_disturbance_profile, CA_entrada_disturbance_profile)

    # --- 3. Resolver o Sistema de EDOs Numericamente ---
    solucao = odeint(reactor_odes, Y0, t_span, args=(params,))

    # Extrair as variáveis de estado da solução
    h_sim = solucao[:, 0]
    T_sim = solucao[:, 1]
    CA_sim = solucao[:, 2]

    # Garantir que altura e concentração não sejam negativas
    h_sim[h_sim < 0] = 0
    CA_sim[CA_sim < 0] = 0

    # --- 4. Calcular Ações de Controle e Setpoints/Distúrbios para Plotagem ---
    Q_entrada_plot = []
    Q_aquecedor_plot = []
    setpoint_nivel_plot = []
    setpoint_temperatura_plot = []
    T_entrada_plot = []
    Q_entrada_base_plot = []

    for i, t_val in enumerate(t_span):
        current_setpoint_nivel = setpoint_nivel_profile(t_val)
        current_setpoint_temperatura = setpoint_temperatura_profile(t_val)
        current_Q_entrada_base = Q_entrada_disturbance_profile(t_val)
        current_T_entrada = T_entrada_disturbance_profile(t_val)

        erro_nivel = current_setpoint_nivel - h_sim[i]
        Q_entrada_control = current_Q_entrada_base + Kp_nivel * erro_nivel
        Q_entrada_plot.append(np.clip(Q_entrada_control, 0.0, Q_entrada_max))

        erro_temp = current_setpoint_temperatura - T_sim[i]
        Q_aquecedor_control = Kp_temp * erro_temp
        Q_aquecedor_plot.append(np.clip(Q_aquecedor_control, Q_resfriador_max, Q_aquecedor_max))

        setpoint_nivel_plot.append(current_setpoint_nivel)
        setpoint_temperatura_plot.append(current_setpoint_temperatura)
        T_entrada_plot.append(current_T_entrada)
        Q_entrada_base_plot.append(current_Q_entrada_base)

    # --- 5. Organizar Resultados em DataFrame (para fácil análise e plotagem) ---
    df_simulacao = pd.DataFrame({
        'Tempo (min)': t_span,
        'Altura (m)': h_sim,
        'Temperatura (°C)': T_sim,
        'Concentração (mol/L)': CA_sim,
        'Setpoint Nível (m)': setpoint_nivel_plot,
        'Setpoint Temperatura (°C)': setpoint_temperatura_plot,
        'Vazão de Entrada Controlada (m³/min)': Q_entrada_plot,
        'Potência Aquecedor Controlada (J/min)': Q_aquecedor_plot,
        'Vazão de Entrada Base (Distúrbio) (m³/min)': Q_entrada_base_plot,
        'Temperatura de Entrada (Distúrbio) (°C)': T_entrada_plot
    })

    print("\n--- Resultados da Simulação (Primeiras 5 linhas) ---")
    print(df_simulacao.head())
    print(f"\nSimulação concluída em {tempo_max} minutos.")

    # --- 6. Visualização dos Resultados ---
    sns.set_style("whitegrid")
    plt.figure(figsize=(14, 12)) # Figura maior para múltiplos gráficos

    # Gráfico 1: Altura do Nível
    plt.subplot(3, 1, 1) # 3 linhas, 1 coluna, 1º gráfico
    sns.lineplot(x='Tempo (min)', y='Altura (m)', data=df_simulacao, label='Altura Real', color='blue', linewidth=2)
    sns.lineplot(x='Tempo (min)', y='Setpoint Nível (m)', data=df_simulacao, label='Setpoint Nível', color='red', linestyle='--', linewidth=1.5)
    plt.ylabel('Altura (m)')
    plt.title('Desempenho do Reator Químico')
    plt.legend(loc='upper right')
    plt.grid(True)

    # Gráfico 2: Temperatura
    plt.subplot(3, 1, 2) # 3 linhas, 1 coluna, 2º gráfico
    sns.lineplot(x='Tempo (min)', y='Temperatura (°C)', data=df_simulacao, label='Temperatura Real', color='green', linewidth=2)
    sns.lineplot(x='Tempo (min)', y='Setpoint Temperatura (°C)', data=df_simulacao, label='Setpoint Temperatura', color='purple', linestyle='--', linewidth=1.5)
    sns.lineplot(x='Tempo (min)', y='Temperatura de Entrada (Distúrbio) (°C)', data=df_simulacao, label='Temp. Entrada (Distúrbio)', color='orange', linestyle=':', linewidth=1)
    plt.ylabel('Temperatura (°C)')
    plt.legend(loc='upper right')
    plt.grid(True)

    # Gráfico 3: Concentração e Vazão de Entrada
    plt.subplot(3, 1, 3) # 3 linhas, 1 coluna, 3º gráfico
    sns.lineplot(x='Tempo (min)', y='Concentração (mol/L)', data=df_simulacao, label='Concentração de A', color='brown', linewidth=2)
    
    # Segundo eixo Y para Vazão de Entrada
    ax2 = plt.gca().twinx()
    sns.lineplot(x='Tempo (min)', y='Vazão de Entrada Controlada (m³/min)', data=df_simulacao, ax=ax2, label='Vazão Entrada Controlada', color='cyan', linestyle='-', linewidth=1.5)
    sns.lineplot(x='Tempo (min)', y='Vazão de Entrada Base (Distúrbio) (m³/min)', data=df_simulacao, ax=ax2, label='Vazão Entrada Base (Distúrbio)', color='darkblue', linestyle=':', linewidth=1)
    
    ax2.set_ylabel('Vazão (m³/min)', color='cyan')
    ax2.tick_params(axis='y', labelcolor='cyan')
    plt.xlabel('Tempo (min)')
    plt.ylabel('Concentração (mol/L)', color='brown')
    plt.tick_params(axis='y', labelcolor='brown')
    ax2.legend(loc='upper left')
    plt.legend(loc='upper right')
    plt.grid(True)

    plt.tight_layout() # Ajusta o layout para evitar sobreposição
    plt.show()

# --- Execução do Mini Projeto Final ---
if __name__ == "__main__":
    simular_sistema_reator()