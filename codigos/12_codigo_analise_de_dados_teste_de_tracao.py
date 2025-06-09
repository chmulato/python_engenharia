# Análise de Dados de Teste de Tração

def calcular_tensao(forcas, area_inicial):
    """Calcula a tensão a partir da força e da área inicial."""
    tensões = [força / area_inicial for força in forcas]  # List Comprehension
    return tensões

def calcular_deformacao(alongamentos, comprimento_inicial):
    """Calcula a deformação a partir do alongamento e do comprimento inicial."""
    deformações = [alongamento / comprimento_inicial for alongamento in alongamentos] # List Comprehension
    return deformações

def calcular_modulo_elasticidade(deformações, tensões, num_pontos=10):
    """
    Estima o módulo de elasticidade a partir da inclinação inicial da curva tensão-deformação.
    Usa os primeiros 'num_pontos' para ajustar uma linha.
    """
    if len(deformações) < num_pontos:
        num_pontos = len(deformações)

    soma_xy = sum(deformações[i] * tensões[i] for i in range(num_pontos))
    soma_x = sum(deformações[i] for i in range(num_pontos))
    soma_y = sum(tensões[i] for i in range(num_pontos))
    soma_x_quadrado = sum(deformações[i]**2 for i in range(num_pontos))

    n = num_pontos
    numerador = n * soma_xy - soma_x * soma_y
    denominador = n * soma_x_quadrado - soma_x**2

    if denominador == 0:
        return 0  # Evitar divisão por zero
    else:
        return numerador / denominador


def estimar_tensao_escoamento(deformações, tensões, offset=0.002):
    """
    Estima a tensão de escoamento usando o método do deslocamento de 0,2%.
    """
    for i in range(len(deformações)):
        if deformações[i] >= (offset):
            # Encontrar a tensão correspondente (linearmente aproximada)
            if i > 0:
                deformacao_anterior = deformações[i-1]
                tensao_anterior = tensões[i-1]
                inclinacao = (tensões[i] - tensao_anterior) / (deformações[i] - deformacao_anterior)
                tensao_escoamento = tensao_anterior + inclinacao * (offset - deformacao_anterior)
                return tensao_escoamento
            else:
                return tensões[0] # Se o primeiro ponto já passou do offset
    return None # Se não encontrar

# 1. Dados de Entrada
forcas = [0, 1000, 2500, 4000, 5500, 7000, 8500, 9000, 8800, 8500]  # Forças em N
alongamentos = [0, 0.2, 0.5, 0.8, 1.1, 1.4, 1.7, 2.0, 2.5, 3.0]  # Alongamentos em mm
area_inicial = 50  # Área da seção transversal inicial em mm²
comprimento_inicial = 50  # Comprimento inicial em mm

# 2. Calcular Tensão e Deformação
tensões = calcular_tensao(forcas, area_inicial)
deformações = calcular_deformacao(alongamentos, comprimento_inicial)

# 3. Determinar o Módulo de Elasticidade
modulo_elasticidade = calcular_modulo_elasticidade(deformações, tensões)

# 4. Determinar a Tensão de Escoamento
tensao_escoamento = estimar_tensao_escoamento(deformações, tensões)

# 5. Saída de Dados
print("Análise de Dados de Teste de Tração\n")
print("Curva Tensão-Deformação:")
for i in range(len(tensões)):
    print(f"Tensão: {tensões[i]:.2f} MPa, Deformação: {deformações[i]:.4f}")

print(f"\nMódulo de Elasticidade: {modulo_elasticidade:.2f} MPa")
print(f"Tensão de Escoamento (0.2%): {tensao_escoamento:.2f} MPa")