import numpy as np
import matplotlib.pyplot as plt
# 1. Simulação de dados
np.random.seed(42)  # Para reprodutibilidade
tempo = np.arange(0, 100, 1)  # Tempo de 0 a 99 segundos
setpoint = np.where(tempo < 50, 50, 70)  # Setpoint muda de 50°C para 70°C em t=50s
temperatura_real = 50 + 0.5 * (tempo - 50) + np.random.normal(0, 1, len(tempo))  # Resposta do sistema com ruído
saida_controlador = np.clip(0.5 * (setpoint - temperatura_real), 0, 100)  # Saída do controlador proporcional
# 2. Criação do gráfico
plt.figure(figsize=(12, 6))
plt.plot(tempo, setpoint, label='Setpoint (Temperatura Desejada)', color='blue', linestyle='--')
plt.plot(tempo, temperatura_real, label='Temperatura Real', color='red')
plt.plot(tempo, saida_controlador, label='Saída do Controlador', color='green')
plt.title('Análise do Desempenho de um Sistema de Controle de Temperatura')
plt.xlabel('Tempo (s)')
plt.ylabel('Temperatura (°C) / Saída do Controlador (%)')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()