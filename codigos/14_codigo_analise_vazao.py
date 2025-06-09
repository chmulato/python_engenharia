import csv
from datetime import datetime
import numpy as np # Importa a biblioteca NumPy para cálculos numéricos eficientes
import matplotlib.pyplot as plt # Importa a biblioteca Matplotlib para gerar gráficos

def ler_dados_vazao(nome_arquivo):
    """
    Lê dados de vazão de um arquivo CSV.

    Args:
        nome_arquivo (str): O nome do arquivo CSV.

    Returns:
        tuple: Uma tupla contendo duas listas (timestamps, vazoes), ou (None, None) em caso de erro.
    """
    timestamps = []
    vazoes = []
    try:
        with open(nome_arquivo, 'r') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            next(leitor_csv)  # Pular o cabeçalho
            for linha in leitor_csv:
                timestamp_str = linha[0]
                vazao = float(linha[1])
                # Converte a string do timestamp para um objeto datetime
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                timestamps.append(timestamp)
                vazoes.append(vazao)
        return timestamps, vazoes
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {nome_arquivo}")
        return None, None
    except (ValueError, IndexError) as e: # Trata erros de conversão ou formato de linha
        print(f"Erro ao processar dados no arquivo {nome_arquivo}: {e}")
        return None, None

def vazao_media(vazoes):
    """Calcula a vazão média de uma lista de vazões."""
    if not vazoes:
        return 0
    # Usa np.mean para calcular a média de forma eficiente
    return np.mean(vazoes)

def vazao_desvio_padrao(vazoes):
    """Calcula o desvio padrão de uma lista de vazões."""
    if not vazoes:
        return 0
    # Usa np.std para calcular o desvio padrão de forma eficiente
    return np.std(vazoes)

def vazao_mediana(vazoes):
    """Calcula a mediana de uma lista de vazões."""
    if not vazoes:
        return 0
    # Usa np.median para calcular a mediana de forma eficiente
    return np.median(vazoes)

def vazao_maxima(timestamps, vazoes):
    """Encontra a vazão máxima e o timestamp em que ocorreu."""
    if not vazoes:
        return None, None
    # Encontra o índice da vazão máxima
    idx_max = np.argmax(vazoes)
    return vazoes[idx_max], timestamps[idx_max]

def vazao_minima(timestamps, vazoes):
    """Encontra a vazão mínima e o timestamp em que ocorreu."""
    if not vazoes:
        return None, None
    # Encontra o índice da vazão mínima
    idx_min = np.argmin(vazoes)
    return vazoes[idx_min], timestamps[idx_min]

def gerar_grafico_vazao(timestamps, vazoes, media, desvio_padrao, maxima_vazao, maxima_tempo, minima_vazao, minima_tempo):
    """
    Gera um gráfico da vazão versus tempo com estatísticas destacadas.

    Args:
        timestamps (list): Lista de objetos datetime para o eixo X.
        vazoes (list): Lista de valores de vazão para o eixo Y.
        media (float): Vazão média.
        desvio_padrao (float): Desvio padrão da vazão.
        maxima_vazao (float): Valor da vazão máxima.
        maxima_tempo (datetime): Timestamp da vazão máxima.
        minima_vazao (float): Valor da vazão mínima.
        minima_tempo (datetime): Timestamp da vazão mínima.
    """
    plt.figure(figsize=(12, 6)) # Define o tamanho da figura do gráfico
    plt.plot(timestamps, vazoes, label='Vazão Medida', color='blue', alpha=0.7) # Plota a série temporal da vazão

    # Adiciona linhas para as estatísticas
    plt.axhline(media, color='red', linestyle='--', label=f'Média: {media:.2f} m³/h')
    plt.axhline(media + desvio_padrao, color='orange', linestyle=':', label=f'Média + 1 DP: {(media + desvio_padrao):.2f} m³/h')
    plt.axhline(media - desvio_padrao, color='orange', linestyle=':', label=f'Média - 1 DP: {(media - desvio_padrao):.2f} m³/h')

    # Marca os pontos de máximo e mínimo
    if maxima_tempo and maxima_vazao is not None:
        plt.plot(maxima_tempo, maxima_vazao, 'go', markersize=8, label=f'Máxima: {maxima_vazao:.2f} m³/h') # 'go' para marcador verde em círculo
    if minima_tempo and minima_vazao is not None:
        plt.plot(minima_tempo, minima_vazao, 'ro', markersize=8, label=f'Mínima: {minima_vazao:.2f} m³/h') # 'ro' para marcador vermelho em círculo

    # Configurações do gráfico
    plt.xlabel('Timestamp') # Rótulo do eixo X
    plt.ylabel('Vazão (m³/h)') # Rótulo do eixo Y
    plt.title('Vazão Volumétrica de Água Limpa ao Longo do Tempo') # Título do gráfico
    plt.grid(True) # Adiciona grade ao gráfico
    plt.legend() # Mostra a legenda
    plt.xticks(rotation=45, ha='right') # Rotaciona os rótulos do eixo X para melhor legibilidade
    plt.tight_layout() # Ajusta o layout para evitar sobreposição
    plt.show() # Exibe o gráfico

# --- Programa Principal ---
if __name__ == "__main__":
    nome_do_arquivo = "vazao_efluente.csv"

    # 1. Leitura do Arquivo CSV
    timestamps, vazoes = ler_dados_vazao(nome_do_arquivo)

    if timestamps and vazoes: # Verifica se os dados foram lidos com sucesso
        # 2. Análise Estatística Avançada
        media = vazao_media(vazoes)
        desvio_padrao = vazao_desvio_padrao(vazoes)
        mediana = vazao_mediana(vazoes)
        maxima_vazao, maxima_tempo = vazao_maxima(timestamps, vazoes)
        minima_vazao, minima_tempo = vazao_minima(timestamps, vazoes)

        # 3. Relatório Final
        print("--- Relatório de Análise de Vazão ---")
        print(f"Vazão Média: {media:.2f} m³/h")
        print(f"Desvio Padrão da Vazão: {desvio_padrao:.2f} m³/h")
        print(f"Mediana da Vazão: {mediana:.2f} m³/h")
        print(f"Vazão Máxima: {maxima_vazao:.2f} m³/h (em {maxima_tempo})")
        print(f"Vazão Mínima: {minima_vazao:.2f} m³/h (em {minima_tempo})")
        print("-------------------------------------\n")

        # 4. Visualização de Dados
        gerar_grafico_vazao(timestamps, vazoes, media, desvio_padrao, maxima_vazao, maxima_tempo, minima_vazao, minima_tempo)
    else:
        print("Não foi possível realizar a análise devido a erros na leitura dos dados.")
