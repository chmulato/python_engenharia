import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 1. Simular antenas e posição real do dispositivo
np.random.seed(42)  # Para reprodutibilidade

# Coordenadas das antenas (x, y)
antennas = np.array([
    [0, 0],
    [100, 0],
    [50, 100],
    [100, 100]
])

# Posição real do dispositivo
real_position = np.array([60, 40])

# 2. Calcular distâncias reais e adicionar ruído (simular ToA)
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2)**2))

# Distâncias reais das antenas ao dispositivo
true_distances = np.array([euclidean_distance(a, real_position) for a in antennas])

# Adiciona ruído gaussiano às distâncias medidas
noise_std = 3  # padrão do ruído
measured_distances = true_distances + np.random.normal(0, noise_std, size=len(antennas))

# 3. Definir a função de erro (mínimos quadrados)
def error_function(position):
    x, y = position
    estimated_distances = np.array([euclidean_distance(np.array([x, y]), a) for a in antennas])
    error = np.sum((estimated_distances - measured_distances)**2)
    return error

# 4. Otimizar a função para encontrar (x, y) estimado
initial_guess = [50, 50]
result = minimize(error_function, initial_guess)
estimated_position = result.x

# 5. Visualizar os resultados
plt.figure(figsize=(8, 8))
plt.scatter(antennas[:, 0], antennas[:, 1], c='blue', label='Antenas')
plt.scatter(*real_position, c='green', label='Posição Real', marker='x', s=100)
plt.scatter(*estimated_position, c='red', label='Posição Estimada', marker='o', s=100)

# Desenhar círculos com distâncias medidas
for i, antenna in enumerate(antennas):
    circle = plt.Circle(antenna, measured_distances[i], color='gray', fill=False, linestyle='--')
    plt.gca().add_artist(circle)
    plt.text(antenna[0]+2, antenna[1]+2, f"A{i+1}", color='blue')

plt.legend()
plt.title("Localização de Dispositivo por Triangulação (ToA)")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.axis('equal')
plt.show()