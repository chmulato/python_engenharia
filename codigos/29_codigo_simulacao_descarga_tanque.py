import numpy as np
from scipy.integrate import odeint # Função para resolver EDOs
import matplotlib.pyplot as plt
import seaborn as sns

def simular_descarga_tanque():
    """
    Simula a descarga de um tanque cilíndrico usando uma EDO e visualiza os resultados.
    """
    print("--- 9.2. Equações Diferenciais Ordinárias (EDOs) ---")
    print("\n--- Exemplo: Descarga de um Tanque Cilíndrico ---")

    # --- 1. Definir os Parâmetros do Tanque e do Orifício ---
    A_T = 1.0       # Área da seção transversal do tanque (m^2)
    A_o = 0.01      # Área do orifício de saída (m^2)
    C_d = 0.6       # Coeficiente de descarga do orifício (adimensional)
    g = 9.81        # Aceleração da gravidade (m/s^2)

    # --- 2. Definir a Equação Diferencial Ordinária (EDO) ---
    # A função deve receber (y, t, *args) onde y é a variável de estado (altura h)
    # e t é a variável independente (tempo). *args são parâmetros adicionais.
    def dHdt(h, t, A_T, A_o, C_d, g):
        """
        Define a EDO para a variação da altura do líquido no tanque.
        dh/dt = - (Ao * Cd * sqrt(2 * g * h)) / AT
        """
        if h <= 0: # Para evitar raiz quadrada de número negativo e simular tanque vazio
            return 0.0
        return - (A_o * C_d * np.sqrt(2 * g * h)) / A_T

    # --- 3. Definir Condições Iniciais e Intervalo de Tempo ---
    h0 = 2.0        # Altura inicial do líquido no tanque (m)
    tempo_max = 200 # Tempo máximo de simulação (s)
    # Array de pontos de tempo onde queremos a solução da EDO
    t = np.linspace(0, tempo_max, 200) # 200 pontos entre 0 e tempo_max

    # --- 4. Resolver a EDO Numericamente usando odeint ---
    # odeint(funcao_edo, condicao_inicial, array_de_tempos, args=(parametros_da_funcao_edo))
    # Retorna um array com a solução para a variável de estado em cada ponto de tempo
    solucao_h = odeint(dHdt, h0, t, args=(A_T, A_o, C_d, g))

    # odeint retorna um array 2D, mesmo para uma única variável.
    # Precisamos extrair a primeira coluna para ter o array de alturas.
    alturas = solucao_h[:, 0]

    # Garantir que a altura não seja negativa (pode acontecer por aproximação numérica)
    alturas[alturas < 0] = 0

    # --- 5. Visualizar a Curva da Altura do Líquido ---
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    plt.plot(t, alturas, label='Altura do Líquido (h)', color='blue', linewidth=2)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Altura (m)')
    plt.title('Descarga de um Tanque Cilíndrico')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("\n--- Resultados da Simulação ---")
    print(f"Altura inicial: {h0:.2f} m")
    print(f"Altura final (após {tempo_max} s): {alturas[-1]:.2f} m")
    # Encontrar o tempo aproximado para esvaziar o tanque
    tempo_esvaziamento = t[np.where(alturas <= 0.01)[0][0]] if np.any(alturas <= 0.01) else "Não esvaziou completamente"
    print(f"Tempo aproximado para esvaziamento: {tempo_esvaziamento} s")


# --- Execução do Exemplo ---
if __name__ == "__main__":
    simular_descarga_tanque()
