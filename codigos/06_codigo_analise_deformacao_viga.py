import matplotlib.pyplot as plt

# Entrada de dados
L = float(input("Digite o comprimento da viga (m): "))
E = float(input("Digite o módulo de elasticidade (Pa): "))
I = float(input("Digite o momento de inércia (m^4): "))
tipo_carregamento = int(input("Digite o tipo de carregamento (1-Uniforme, 2-Pontual): "))

if tipo_carregamento == 1:
    w = float(input("Digite a intensidade da carga uniforme (N/m): "))
    P = 0  # Apenas para manter a consistência das variáveis
elif tipo_carregamento == 2:
    P = float(input("Digite a magnitude da carga pontual (N): "))
    w = 0  # Apenas para manter a consistência das variáveis
else:
    print("Tipo de carregamento inválido.")
    exit()

# Cálculo da deflexão
num_pontos = 100  # Número de pontos para calcular a deflexão
x_valores = [i * L / num_pontos for i in range(num_pontos + 1)]  # Lista de posições x
y_valores = []  # Lista para armazenar os valores de deflexão

for x in x_valores:
    if tipo_carregamento == 1:
        y = (w / (24 * E * I)) * (-x**4 + 2 * L * x**3 - L**3 * x)
    elif tipo_carregamento == 2:
        if 0 <= x <= L / 2:
            y = (P * x / (48 * E * I)) * (3 * L**2 - 4 * x**2)
        else:
            y = (P * (L - x) / (48 * E * I)) * (3 * L**2 - 4 * (L - x)**2)
    y_valores.append(y)

# Geração do gráfico
plt.plot(x_valores, y_valores)
plt.title("Deflexão da Viga")
plt.xlabel("Posição (m)")
plt.ylabel("Deflexão (m)")
plt.grid(True)
plt.savefig("deflexao_viga.png")  # Salva o gráfico como PNG
plt.show()

# Saída de dados
print("\nComprimento da viga:", L, "m")
print("Módulo de elasticidade:", E, "Pa")
print("Momento de inércia:", I, "m^4")
if tipo_carregamento == 1:
    print("Carga uniforme:", w, "N/m")
elif tipo_carregamento == 2:
    print("Carga pontual:", P, "N")
print("Deflexão máxima:", max(y_valores), "m")
print("Gráfico da deflexão salvo como deflexao_viga.png")