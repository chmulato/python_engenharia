import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Definir os Parâmetros do Reator e da Reação (da Tarefa 1) ---
AT = 5.0        # Área da seção transversal do reator (m^2)
H_MAX = 2.0     # Altura máxima do reator (m)
rho = 1000.0    # Densidade do líquido (kg/m^3)
Cp = 4.186      # Capacidade calorífica do líquido (kJ/kg.°C)
Cp_J_kg_C = Cp * 1000 # Convertendo kJ/kg.°C para J/kg.°C

# Parâmetros da Reação Química
k0 = 1.0e10     # Fator pré-exponencial da constante de velocidade (min^-1)
Ea_R = 8000.0   # Energia de ativação / Constante dos gases (K)
delta_H_reacao = -50000.0 # Entalpia de reação (J/mol) - Negativo para exotérmica

# Parâmetros de Vazão e Temperatura de Entrada
Q_entrada_base = 0.1 # Vazão volumétrica de entrada base (m^3/min)
T_entrada_const = 25.0     # Temperatura da corrente de entrada (°C)
CA_entrada_const = 1.0     # Concentração do reagente A na entrada (mol/L)

# Parâmetros do Orifício de Saída
Ao = 0.01       # Área do orifício de saída (m^2)
Cd = 0.6        # Coeficiente de descarga do orifício (adimensional)
g = 9.81 * 60**2 # Aceleração da gravidade (m/min^2)

# Parâmetros do Aquecedor/Resfriador
Q_aquecedor_max = 50000.0 # Potência máxima do aquecedor (J/min)

# Parâmetros de Controle (placeholders para as EDOs)
Q_aquecedor_control = 0.0 # Placeholder: calor do aquecedor no tempo t
Q_entrada_control = Q_entrada_base # Placeholder: vazão de entrada no tempo t
T_entrada_control = T_entrada_const # Placeholder: temperatura de entrada no tempo t
CA_entrada_control = CA_entrada_const # Placeholder: concentração de entrada no tempo t

# --- 2. Implementar a função que descreve o sistema de EDOs acopladas ---
def reactor_odes(Y, t, params):
    """
    Define o sistema de Equações Diferenciais Ordinárias (EDOs) acopladas
    para o reator químico.
    """
    h, T, CA = Y # Desempacotar as variáveis de estado

    # Desempacotar os parâmetros
    AT, Ao, Cd, g, rho, Cp_J_kg_C, k0, Ea_R, delta_H_reacao, \
    Q_aquecedor_func, Q_entrada_func, T_entrada_func, CA_entrada_func = params

    # --- Cálculos Intermediários ---
    # Vazão de Entrada (pode ser uma função do tempo)
    Q_entrada = Q_entrada_func(t)

    # Vazão de Saída (Lei de Torricelli, depende da altura)
    if h <= 0:
        Q_saida = 0.0
    else:
        Q_saida = Cd * Ao * np.sqrt(2 * g * h)
    
    # Volume de Líquido no Reator (depende da altura)
    V_liquido = AT * h
    # Evitar divisão por zero se o tanque estiver vazio
    if V_liquido <= 1e-6:
        V_liquido = 1e-6

    # Constante de Velocidade da Reação (Arrhenius, depende da temperatura)
    k_arrhenius = k0 * np.exp(-Ea_R / (T + 273.15))

    # Taxa de Reação (mol/L.min)
    r_A = k_arrhenius * CA

    # Calor Gerado/Consumido pela Reação (J/min)
    Q_reacao = (-delta_H_reacao) * r_A * V_liquido

    # Calor Fornecido pelo Aquecedor (J/min)
    Q_aquecedor = Q_aquecedor_func(t)

    # Temperatura e Concentração de Entrada
    T_entrada = T_entrada_func(t)
    CA_entrada = CA_entrada_func(t)

    # --- EDOs ---
    # 1. dh/dt (Balanço de Massa Total)
    dhdt = (Q_entrada - Q_saida) / AT

    # 2. dCA/dt (Balanço de Massa para Componente A)
    dCAdt = (Q_entrada * CA_entrada - Q_saida * CA - V_liquido * r_A) / V_liquido
    if h <= 0:
        dCAdt = 0.0

    # 3. dT/dt (Balanço de Energia)
    dTdt = (Q_entrada * (T_entrada - T) / V_liquido) + \
           (Q_reacao / (V_liquido * rho * Cp_J_kg_C)) + \
           (Q_aquecedor / (V_liquido * rho * Cp_J_kg_C))
    if h <= 0:
        dTdt = 0.0

    return [dhdt, dTdt, dCAdt]

# --- Exemplo de uso da função EDO (para teste, não é a simulação completa) ---
if __name__ == "__main__":
    print("--- Teste da Função de EDOs do Reator ---")

    # Parâmetros (usando os definidos acima)
    params_test = (AT, Ao, Cd, g, rho, Cp_J_kg_C, k0, Ea_R, delta_H_reacao,
                   lambda t: Q_aquecedor_control, # Função placeholder para aquecedor
                   lambda t: Q_entrada_control,   # Função placeholder para Q_entrada
                   lambda t: T_entrada_control,   # Função placeholder para T_entrada
                   lambda t: CA_entrada_control)  # Função placeholder para CA_entrada

    # Condições iniciais de teste
    h_test = 1.0
    T_test = 50.0
    CA_test = 0.5
    Y_test = [h_test, T_test, CA_test]
    t_test = 0.0 # Tempo inicial

    # Calcular as derivadas no tempo inicial
    derivadas = reactor_odes(Y_test, t_test, params_test)

    print(f"\nVariáveis de Estado Iniciais: h={h_test:.2f}m, T={T_test:.2f}°C, CA={CA_test:.2f}mol/L")
    print(f"Derivadas Calculadas (dh/dt, dT/dt, dCA/dt):")
    print(f"  dh/dt = {derivadas[0]:.4f} m/min")
    print(f"  dT/dt = {derivadas[1]:.4f} °C/min")
    print(f"  dCA/dt = {derivadas[2]:.4f} mol/L.min")

    # O restante da simulação (chamada ao odeint, lógica de controle, visualização)
    # será implementado nas próximas tarefas.