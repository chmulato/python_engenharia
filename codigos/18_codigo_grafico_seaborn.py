import seaborn as sns
import pandas as pd
import numpy as np  # Adicione esta linha
import matplotlib.pyplot as plt  # Adicione esta linha

# Dados de exemplo
dados = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100))
})

# Criação do gráfico
sns.lineplot(data=dados, x='x', y='y')
plt.title('Gráfico de Seno com Seaborn')
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.grid()
plt.show()