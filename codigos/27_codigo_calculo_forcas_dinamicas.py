import numpy as np
import matplotlib.pyplot as plt
# 1. Definição dos parâmetros aerodinâmicos
rho = 1.225  # Densidade do ar em kg/m³
S = 20.0  # Área da asa em m²
CL = 1.2  # Coeficiente de Sustentação
CD = 0.05  # Coeficiente de Arrasto
# 2. Criação do array de velocidades
V = np.linspace(0, 100, 500)  # Velocidades de 0 a 100 m/s
# 3. Cálculo das forças de Sustentação e Arrasto
L = 0.5 * rho * V**2 * S * CL  # Força de Sustentação
D = 0.5 * rho * V**2 * S * CD  # Força de Arrasto
# 4. Visualização das forças
plt.figure(figsize=(12, 6))
plt.plot(V, L, label='Sustentação (Lift)', color='blue')
plt.plot(V, D, label='Arrasto (Drag)', color='red')
plt.title('Forças Aerodinâmicas em Função da Velocidade do Ar')
plt.xlabel('Velocidade do Ar (m/s)')
plt.ylabel('Força (N)')
plt.legend()
plt.grid()
plt.show()
