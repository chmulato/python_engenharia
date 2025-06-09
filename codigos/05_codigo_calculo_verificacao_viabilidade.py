# Entrada de dados
comprimento = float(input("Digite o comprimento do terreno (m): "))
largura = float(input("Digite a largura do terreno (m): "))
area_minima = float(input("Digite a área mínima permitida para construção (m²): "))

# Cálculos
area_terreno = comprimento * largura
perimetro_terreno = 2 * (comprimento + largura)

# Verificação de viabilidade
viabilidade = area_terreno >= area_minima and perimetro_terreno < 100

# Saída de dados
print(f"\nÁrea do terreno: {area_terreno:.2f} m²")
print(f"Perímetro do terreno: {perimetro_terreno:.2f} m")
print(f"Terreno viável para construção: {viabilidade}")