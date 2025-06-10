import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns

def simular_tanque_entrada_saida():
    """
    Simula a dinâmica da altura do líquido em um tanque com entrada e saída,
    usando uma EDO e visualiza os resultados.
    """
    print("--- 10.1. Estudo de Caso: Tanque com Entrada e Saída ---")

    # --- 1. Definir os Parâmetros do Tanque e do Processo ---
    A_T = 5.0       # Área da seção transversal do tanque (m^2)
    A_o = 0.02      # Área do orifício de saída (m^2)
    C_d = 0.65      # Coeficiente de descarga do orifício (adimensional)
    g = 9.81        # Aceleração da gravidade (m/s^2)

    # --- 2. Definir a Função da Vazão de Entrada (Q_entrada) ---
    # Pode ser constante ou variar no tempo.
    # Exemplo: Vazão de entrada constante
    Q_entrada_constante = 0.1 # m^3/s

    # Exemplo: Vazão de entrada que muda em um certo tempo
    def Q_entrada_funcao_tempo(t_atual):
        if t_atual < 50:
            return 0.1 # m^3/s
        else:
            return 0.05 # m^3/s (reduz a vazão de entrada após 50s)

    # --- 3. Definir a Equação Diferencial Ordinária (EDO) ---
    # dh/dt = (Q_entrada - Q_saida) / AT
    # Q_saida = Cd * Ao * sqrt(2 * g * h)
    def dHdt(h, t, A_T, A_o, C_d, g, Q_entrada_func):
        """
        Define a EDO para a variação da altura do líquido no tanque.
        """
        # Vazão de entrada no tempo atual
        Q_entrada = Q_entrada_func(t) # Usando a função de entrada variável no tempo

        # Vazão de saída (Lei de Torricelli)
        # Condicional para evitar raiz de número negativo se h for <= 0
        if h <= 0:
            Q_saida = 0.0
        else:
            Q_saida = C_d * A_o * np.sqrt(2 * g * h)
        
        # EDO
        dh_dt = (Q_entrada - Q_saida) / A_T
        return dh_dt

    # --- 4. Definir Condição Inicial e Intervalo de Tempo ---
    h0 = 0.5        # Altura inicial do líquido no tanque (m)
    tempo_max = 200 # Tempo máximo de simulação (s)
    t = np.linspace(0, tempo_max, 300) # 300 pontos de tempo para a solução

    # --- 5. Resolver a EDO Numericamente usando odeint ---
    # Passamos a função Q_entrada_funcao_tempo como um dos argumentos da EDO
    solucao_h = odeint(dHdt, h0, t, args=(A_T, A_o, C_d, g, Q_entrada_funcao_tempo))

    # odeint retorna um array 2D, extraímos a primeira coluna para ter o array de alturas.
    alturas = solucao_h[:, 0]

    # Garantir que a altura não seja negativa (pode acontecer por aproximação numérica)
    alturas[alturas < 0] = 0

    # --- 6. Visualizar a Curva da Altura do Líquido ---
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    plt.plot(t, alturas, label='Altura do Líquido (h)', color='blue', linewidth=2)

    # Plotar a vazão de entrada para contextualizar a mudança
    Q_entrada_plot = np.array([Q_entrada_funcao_tempo(ti) for ti in t])
    # Criar um segundo eixo Y para a vazão de entrada
    ax2 = plt.gca().twinx()
    ax2.plot(t, Q_entrada_plot, label='Vazão de Entrada (Q_in)', color='red', linestyle=':', linewidth=1.5)
    ax2.set_ylabel('Vazão de Entrada (m³/s)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Altura (m)', color='blue')
    plt.tick_params(axis='y', labelcolor='blue')
    plt.title('Dinâmica da Altura do Líquido em um Tanque')
    plt.legend(loc='upper left') # Ajusta a posição da legenda para não sobrepor
    ax2.legend(loc='upper right')
    plt.grid(True)
    plt.show()

    print("\n--- Resultados da Simulação ---")
    print(f"Altura inicial: {h0:.2f} m")
    print(f"Altura final (após {tempo_max} s): {alturas[-1]:.2f} m")
    # Encontrar o tempo aproximado para atingir o regime permanente (se houver)
    # Isso é mais complexo, mas podemos verificar se a altura está estável no final
    if abs(alturas[-1] - alturas[-50]) < 0.01: # Se a variação nas últimas 50 amostras for pequena
        print("O tanque parece ter atingido um regime permanente.")
    else:
        print("O tanque ainda está em transiente ou esvaziando/enchendo.")


# --- Execução do Exemplo ---
if __name__ == "__main__":
    simular_tanque_entrada_saida()