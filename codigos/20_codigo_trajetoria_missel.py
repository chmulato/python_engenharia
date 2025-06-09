# Código para Trajetória de um Míssil Balístico
# Este código gera gráficos 2D da trajetória de um míssil balístico, analisando a variação da velocidade ao longo do tempo.
# Os dados devem estar em um arquivo CSV com colunas 'Posicao_X', 'Posicao_Y', 'Tempo' e 'Velocidade'.
# Certifique-se de que o arquivo '20_arquivo_trajetoria_missel.csv' esteja no mesmo diretório do script.
# O código utiliza as bibliotecas pandas, matplotlib e seaborn para manipulação de dados e visualização gráfica.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 1. Leitura dos dados
caminho = input("Digite o caminho completo do arquivo CSV: ")
df = pd.read_csv(caminho)
# Se o arquivo estiver no mesmo diretório do script, você pode usar:
# df = pd.read_csv('20_arquivo_trajetoria_missel.csv')
df = pd.read_csv('20_arquivo_trajetoria_missel.csv')
# 2. Gráfico 2D da trajetória do míssil
plt.figure(figsize=(10, 6))
plt.plot(df['Posicao_X'], df['Posicao_Y'], marker='o', label='Trajetória do Míssil')
plt.title('Trajetória do Míssil Balístico')
plt.xlabel('Posição X (m)')
plt.ylabel('Posição Y (m)')
plt.grid()
plt.legend()
plt.show()
# 3. Análise da variação da velocidade ao longo do tempo
plt.figure(figsize=(10, 6))
plt.plot(df['Tempo'], df['Velocidade'], marker='o', color='orange', label='Velocidade')
plt.title('Variação da Velocidade ao Longo do Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.grid()
plt.legend()
plt.show()
# 4. Gráfico de dispersão da velocidade em função do tempo
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Tempo', y='Velocidade', color='green', s=100)
plt.title('Velocidade do Míssil em Função do Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.grid()
plt.show()
