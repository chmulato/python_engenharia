import matplotlib.pyplot as plt

# Dados de exemplo
categorias = ['A', 'B', 'C', 'D']
valores = [10, 20, 15, 25]

# Criando o gráfico
plt.bar(categorias, valores)
plt.title("Comparação de Valores entre Categorias")
plt.xlabel("Categorias")
plt.ylabel("Valores")
plt.grid()
plt.show()