import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Definir os Parâmetros do Reator e da Reação ---

# Parâmetros Físicos do Reator
AT = 5.0        # Área da seção transversal do reator (m^2)
H_MAX = 2.0     # Altura máxima do reator (m)
rho = 1000.0    # Densidade do líquido (kg/m^3) - assumindo água
Cp = 4.186      # Capacidade calorífica do líquido (kJ/kg.°C) - assumindo água

# Parâmetros da Reação Química (A -> Produtos, exotérmica)
k0 = 1.0e10     # Fator pré-exponencial da constante de velocidade (min^-1)
Ea_R = 8000.0   # Energia de ativação / Constante dos gases (K)
                # (Ea em J/mol, R em J/mol.K, então Ea/R em K)
delta_H_reacao = -50000.0 # Entalpia de reação (J/mol) - Negativo para exotérmica

# Parâmetros de Vazão e Temperatura de Entrada
Q_entrada_base = 0.1 # Vazão volumétrica de entrada base (m^3/min)
T_entrada = 25.0     # Temperatura da corrente de entrada (°C)
CA_entrada = 1.0     # Concentração do reagente A na entrada (mol/L)

# Parâmetros do Orifício de Saída (para controle de nível)
Ao = 0.01       # Área do orifício de saída (m^2)
Cd = 0.6        # Coeficiente de descarga do orifício (adimensional)
g = 9.81 * 60**2 # Aceleração da gravidade (m/min^2) - convertida para min^2

# Parâmetros do Aquecedor/Resfriador (para controle de temperatura)
Q_aquecedor_max = 50000.0 # Potência máxima do aquecedor (J/min)
                          # (Assumindo que 1W = 1 J/s, então 1 J/min = 1/60 W)
                          # Ou, se Q_aquecedor_max é em W, converter para J/min: Q_aquecedor_max * 60

# Parâmetros de Controle (Exemplo de P, PI, PID - simplificado para este projeto)
# Ganhos do controlador de Nível (Proporcional)
Kp_nivel = 0.5

# Ganhos do controlador de Temperatura (Proporcional)
Kp_temp = 100.0

# Setpoints (Valores desejados)
setpoint_nivel = 1.0 # m
setpoint_temperatura = 60.0 # °C

print("--- Parâmetros do Reator e da Reação Definidos ---")
print(f"Área do Reator (AT): {AT} m^2")
print(f"Altura Máxima do Reator (H_MAX): {H_MAX} m")
print(f"Densidade do Líquido (rho): {rho} kg/m^3")
print(f"Capacidade Calorífica (Cp): {Cp} kJ/kg.°C")
print(f"Fator Pré-exponencial (k0): {k0}")
print(f"Ea/R: {Ea_R} K")
print(f"Entalpia de Reação (delta_H_reacao): {delta_H_reacao} J/mol")
print(f"Vazão de Entrada Base (Q_entrada_base): {Q_entrada_base} m^3/min")
print(f"Temperatura de Entrada (T_entrada): {T_entrada} °C")
print(f"Concentração de Entrada (CA_entrada): {CA_entrada} mol/L")
print(f"Área do Orifício (Ao): {Ao} m^2")
print(f"Coeficiente de Descarga (Cd): {Cd}")
print(f"Gravidade (g): {g} m/min^2")
print(f"Potência Máxima Aquecedor (Q_aquecedor_max): {Q_aquecedor_max} J/min")
print(f"Ganho Proporcional Nível (Kp_nivel): {Kp_nivel}")
print(f"Ganho Proporcional Temperatura (Kp_temp): {Kp_temp}")
print(f"Setpoint Nível: {setpoint_nivel} m")
print(f"Setpoint Temperatura: {setpoint_temperatura} °C")

# O restante do código (EDOs, lógica de controle, simulação, visualização)
# virá nas próximas tarefas, utilizando esses parâmetros.