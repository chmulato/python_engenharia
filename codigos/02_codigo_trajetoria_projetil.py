import matplotlib.pyplot as plt
import math

# Dados de entrada (tipos float e int)
velocidade_inicial = 20.0  # m/s
angulo_graus = 45       # graus
angulo_radianos = math.radians(angulo_graus) # conversão para radianos
gravidade = 9.81       # m/s²
tempo_total = (2 * velocidade_inicial * math.sin(angulo_radianos)) / gravidade

# Listas para armazenar os pontos da trajetória (listas de floats)
tempos = []
posicoes_x = []
posicoes_y = []

# Cálculo da trajetória
intervalo_tempo = 0.1  # segundos
tempo = 0.0

while tempo <= tempo_total:
    tempos.append(tempo)
    posicao_x = velocidade_inicial * math.cos(angulo_radianos) * tempo
    posicao_y = velocidade_inicial * math.sin(angulo_radianos) * tempo - 0.5 * gravidade * tempo**2
    posicoes_x.append(posicao_x)
    posicoes_y.append(posicao_y)
    tempo += intervalo_tempo

# Nome do projétil (string)
nome_projétil = "Projétil A"

# Geração do gráfico
plt.plot(posicoes_x, posicoes_y)
plt.title("Trajetória de um Projétil")
plt.xlabel("Distância Horizontal (m)")
plt.ylabel("Altura (m)")
plt.grid(True)

# Adicionando informações textuais ao gráfico
plt.text(0, max(posicoes_y) * 0.9, f"Velocidade Inicial: {velocidade_inicial} m/s", fontsize=9)
plt.text(0, max(posicoes_y) * 8, f"Ângulo: {angulo_graus} graus", fontsize=9)
plt.text(0, max(posicoes_y) * 0.7, nome_projétil, fontsize=12, color='red')

plt.show()

# Imprimindo informações relevantes (demonstração de uso de tipos)
print(f"Tempo total de voo: {tempo_total:.2f} s")  # Formatação de float
print(f"Tipo da variável 'nome_projétil': {type(nome_projétil)}") # Mostrando o tipo
print(f"A altura máxima atingida foi: {max(posicoes_y):.2f} m")