indice_poluicao = float(input("Digite o índice de poluição do ar: "))

if indice_poluicao <= 50:
    print("Qualidade do ar: Boa")
elif indice_poluicao <= 100:
    print("Qualidade do ar: Moderada")
elif indice_poluicao <= 150:
    print("Qualidade do ar: Insatisfatória")
elif indice_poluicao <= 200:
    print("Qualidade do ar: Ruim")
else:
    print("Qualidade do ar: Muito Ruim")