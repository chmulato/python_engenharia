import numpy as np
from scipy.optimize import fminbound
import matplotlib.pyplot as plt
import seaborn as sns

def otimizar_area_trocador_calor():
    """
    Otimiza a área de transferência de calor de um trocador de calor
    minimizado uma função de custo total usando scipy.optimize.fminbound.
    """
    print("--- 9.4. Otimização de Funções com scipy.optimize ---")
    print("\n--- Exemplo: Otimização da Área de Trocador de Calor ---")

    # --- 1. Definir as Constantes do Problema ---
    k1 = 100.0  # Custo por unidade de área ($/m^2$)
    k2 = 50000.0 # Constante relacionada ao custo operacional ($ \cdot m^4 / ano$)

    # --- 2. Definir a Função Objetivo (Custo Total) ---
    def custo_total(A, k1, k2):
        """
        Função objetivo a ser minimizada: C_total(A) = k1 * A + k2 / (A**2)
        """
        return k1 * A + k2 / (A**2)

    # --- 3. Definir o Intervalo de Busca para a Área (A) ---
    # A área deve ser positiva. Escolhemos um intervalo razoável.
    area_min = 1.0   # m^2
    area_max = 50.0  # m^2

    # --- 4. Utilizar fminbound para Encontrar o Mínimo ---
    # fminbound(func, x1, x2, args=())
    # func: função a ser minimizada
    # x1, x2: limites do intervalo de busca
    # args: argumentos adicionais a serem passados para func
    resultado_otimizacao = fminbound(custo_total, area_min, area_max, args=(k1, k2))

    area_otima = resultado_otimizacao
    custo_minimo = custo_total(area_otima, k1, k2)

    print("\n--- Resultados da Otimização ---")
    print(f"Área de transferência de calor ótima: {area_otima:.2f} m^2")
    print(f"Custo total mínimo correspondente: ${custo_minimo:.2f} / ano")

    # --- 5. Visualizar a Função Custo e o Ponto de Mínimo ---
    sns.set_style("whitegrid")
    area_plot = np.linspace(area_min * 0.8, area_max * 1.2, 200) # Intervalo maior para visualização
    custo_plot = custo_total(area_plot, k1, k2)

    plt.figure(figsize=(10, 6))
    plt.plot(area_plot, custo_plot, label='Custo Total (C(A))', color='blue')
    plt.scatter(area_otima, custo_minimo, color='red', marker='o', s=100, label=f'Mínimo em A = {area_otima:.2f} m^2')
    plt.xlabel('Área de Transferência de Calor (m^2)')
    plt.ylabel('Custo Total ($/ano)')
    plt.title('Otimização da Área de Trocador de Calor')
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Execução do Exemplo ---
if __name__ == "__main__":
    otimizar_area_trocador_calor()