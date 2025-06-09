import matplotlib.pyplot as plt

# Dados de exemplo
tempo = [0, 1, 2, 3, 4, 5]
velocidade = [0, 10, 20, 30, 40, 50]

# Criando o gráfico
plt.plot(tempo, velocidade)
plt.title("Variação da Velocidade ao Longo do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Velocidade (m/s)")
plt.grid()
plt.show()