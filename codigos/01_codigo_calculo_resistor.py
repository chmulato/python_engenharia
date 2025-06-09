# Definição das variáveis

# Corrente elétrica (float)
corrente = 2.0  # Amperes

# Resistência elétrica (float)
resistencia = 10.0  # Ohms

# Limite de potência (float)
potencia_limite = 20.0  # Watts

# Nome do resistor (string)
nome_resistor = "R1"

# Cálculo da tensão (float)
tensao = corrente * resistencia

# Cálculo da potência (float)
potencia = tensao * corrente

# Verificação da potência (bool)
potencia_excede_limite = potencia > potencia_limite

# Exibição dos resultados
print("Cálculo da Tensão e Potência em um Resistor")
print("------------------------------------------")
print("Nome do Resistor:", nome_resistor)
print("Corrente (A):", corrente)
print("Resistência (Ω):", resistencia)
print("Tensão (V):", tensao)
print("Potência (W):", potencia)
print("Potência excede o limite?", potencia_excede_limite)

# Conversão de tipo (demonstração)
# Converter a tensão para inteiro (truncando a parte decimal)
tensao_inteira = int(tensao)
print("Tensão (V, inteiro):", tensao_inteira)