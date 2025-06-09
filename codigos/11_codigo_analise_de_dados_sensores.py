# Análise de Dados de Sensores de Tensão

def calcular_media(tensões):
    """Calcula a média de uma lista de tensões."""
    return sum(tensões) / len(tensões)

def calcular_maximo(tensões):
    """Calcula o valor máximo de uma lista de tensões."""
    return max(tensões)

def calcular_minimo(tensões):
    """Calcula o valor mínimo de uma lista de tensões."""
    return min(tensões)

def verificar_anomalias(tensões, faixa_aceitavel):
    """Verifica se há tensões fora da faixa aceitável.

    Args:
        tensões (list): Lista de leituras de tensão.
        faixa_aceitavel (tuple): Tupla contendo a tensão mínima e máxima aceitáveis.

    Returns:
        list: Lista de índices das tensões fora da faixa.
    """
    anomalias = []
    for i, tensão in enumerate(tensões):
        if tensão < faixa_aceitavel[0] or tensão > faixa_aceitavel[1]:
            anomalias.append(i)
    return anomalias


# 1. Armazenamento dos Dados dos Sensores
# Dicionário: Chave = Nome do Sensor (string), Valor = Lista de Tensões (float)
dados_sensores = {
    "Sensor_A": [120.5, 121.0, 118.9, 122.1, 115.5],  # Lista de tensões
    "Sensor_B": [220.2, 219.8, 221.1, 218.5, 225.0],  # Lista de tensões
    "Sensor_C": [135.7, 136.0, 134.9, 137.2, 133.3]   # Lista de tensões
}

# Tupla: Faixa de Tensão Aceitável (mínimo, máximo)
faixa_tensão_aceitavel = (117.0, 222.0)


# 2. Cálculo de Estatísticas e 3. Identificação de Anomalias
print("Análise de Dados de Sensores de Tensão\n")

for sensor, tensões in dados_sensores.items():
    print(f"--- Sensor: {sensor} ---")
    media = calcular_media(tensões)
    maximo = calcular_maximo(tensões)
    minimo = calcular_minimo(tensões)
    print(f"Média: {media:.2f} V")
    print(f"Máximo: {maximo:.2f} V")
    print(f"Mínimo: {minimo:.2f} V")

    anomalias = verificar_anomalias(tensões, faixa_tensão_aceitavel)
    if anomalias:
        print(f"ALERTA: Anomalias detectadas nas leituras: {anomalias}")
    else:
        print("Nenhuma anomalia detectada.")
    print()


# Exemplo de acesso aos dados:
# print(dados_sensores["Sensor_A"][0]) # Acessa a primeira leitura do Sensor_A