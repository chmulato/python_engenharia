# Entrada de dados
ll = float(input("Digite o Limite de Liquidez (LL): "))
ip = float(input("Digite o Índice de Plasticidade (IP): "))

# Classificação do solo
if ll >= 50 and ip >= 7:
    classificacao = "Argila"
elif ll < 50 and 4 <= ip < 7:
    classificacao = "Silte"
else:
    classificacao = "Solo Não Plástico"

# Saída de dados
print(f"\nLimite de Liquidez (LL): {ll:.2f}")
print(f"Índice de Plasticidade (IP): {ip:.2f}")
print(f"Classificação do Solo: {classificacao}")