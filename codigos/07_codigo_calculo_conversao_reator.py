# Entrada de dados
nome_reagente = input("Digite o nome do reagente: ")
quantidade_inicial = float(input("Digite a quantidade inicial de " + nome_reagente + " (mols): "))
quantidade_final = float(input("Digite a quantidade final de " + nome_reagente + " (mols): "))
tipo_reator = input("Digite o tipo do reator: ")
tempo_reacao = float(input("Digite o tempo de reação (minutos): "))

# Cálculo da conversão
conversao = (quantidade_inicial - quantidade_final) / quantidade_inicial

# Saída de dados
print("\nReagente:", nome_reagente)
print(f"Quantidade Inicial: {quantidade_inicial:.2f} mols")
print(f"Quantidade Final: {quantidade_final:.2f} mols")
print(f"Conversão: {conversao * 100:.2f} %")
print("Tipo do Reator:", tipo_reator)
print("Tempo de Reação:", tempo_reacao, "minutos")