# Este código cria um histograma usando Matplotlib.
# Os dados são definidos na lista 'dados', e o histograma é exibido com título e rótulos nos eixos.
# O método plt.hist() é usado para criar o histograma, com 5 intervalos (bins) e bordas pretas.
# O método plt.show() exibe o gráfico.
# Este código cria um histograma usando Matplotlib.
import matplotlib.pyplot as plt

# Dados de exemplo
dados = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]

# Criando o gráfico
plt.hist(dados, bins=5, edgecolor='black')
plt.title("Histograma de Frequência")
plt.xlabel("Valores")
plt.ylabel("Frequência")
plt.grid()
plt.show()
