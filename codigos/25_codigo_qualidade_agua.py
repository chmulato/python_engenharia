import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 1. Leitura dos dados
##caminho = input("Digite o caminho completo do arquivo CSV: ")
##df = pd.read_csv(caminho)
# Se o arquivo estiver no mesmo diretório do script, você pode usar:
#  df = pd.read_csv('25_arquivo_qualidade_agua.csv')
df = pd.read_csv('25_arquivo_qualidade_agua.csv')
# Convertendo a coluna Timestamp para o tipo datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
# 2. Gráfico de linha para variação do pH ao longo do tempo
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Timestamp', y='pH', hue='Ponto_Amostragem', marker='o')
plt.title('Variação do pH ao Longo do Tempo')
plt.xlabel('Data e Hora')
plt.ylabel('pH')
plt.xticks(rotation=45)
plt.grid()
plt.legend(title='Ponto de Amostragem')
plt.tight_layout()
plt.show()
# 3. Gráfico de barras para comparar os níveis de oxigênio dissolvido
plt.figure(figsize=(8, 6))
sns.barplot(data=df, x='Ponto_Amostragem', y='Oxigenio_Dissolvido_mgL', ci=None)
plt.title('Comparação dos Níveis de Oxigênio Dissolvido entre Pontos de Amostragem')
plt.xlabel('Ponto de Amostragem')
plt.ylabel('Oxigênio Dissolvido (mg/L)')
plt.grid()
plt.tight_layout()
plt.show()
# 4. Gráfico de dispersão para relação entre turbidez e temperatura
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='Turbidez_NTU', y='Temperatura_C', hue='Ponto_Amostragem', s=100)
plt.title('Relação entre Turbidez e Temperatura da Água')
plt.xlabel('Turbidez (NTU)')
plt.ylabel('Temperatura (°C)')
plt.grid()
plt.legend(title='Ponto de Amostragem')
plt.tight_layout()
plt.show()