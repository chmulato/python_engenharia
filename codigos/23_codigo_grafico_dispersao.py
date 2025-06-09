# Este código cria um gráfico de dispersão simples usando Matplotlib.
# Os pontos são definidos pelas listas x e y, e o gráfico é exibido com título e rótulos nos eixos. 
# O método plt.scatter() é usado para criar o gráfico de dispersão.
# O método plt.show() exibe o gráfico.
import matplotlib.pyplot as plt
# Dados de exemplo
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]
# Criando o gráfico
plt.scatter(x, y)
plt.title("Gráfico de Dispersão")
plt.xlabel("Variável X")
plt.ylabel("Variável Y")
plt.grid()
plt.show()
