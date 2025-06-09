import pandas as pd

def analisar_sistema_eletrico(nome_arquivo):
    """
    Analisa dados de tensão e corrente de um sistema elétrico a partir de um arquivo CSV.

    Args:
        nome_arquivo (str): O nome do arquivo CSV.
    """

    try:
        # 1. Ler o arquivo CSV para um DataFrame
        df = pd.read_csv(nome_arquivo, parse_dates=['Timestamp'])  # Converter Timestamp para datetime

        # 2. Exibir informações básicas do DataFrame
        print("--- Informações Básicas ---")
        print(df.head())  # Primeiras linhas
        print(df.info())  # Resumo das colunas

        # 3. Análise Estatística
        print("\n--- Análise Estatística ---")
        print(df.describe())  # Estatísticas descritivas

        # 4. Agregação de Dados
        print("\n--- Agregação de Dados ---")
        media_tensao_barra = df.groupby('Barra')['Tensão_V'].mean()
        print("Média de tensão por barra:\n", media_tensao_barra)

        max_corrente_barra = df.groupby('Barra')['Corrente_A'].max()
        print("\nMáxima corrente por barra:\n", max_corrente_barra)

        # 5. Filtragem de Dados
        print("\n--- Filtragem de Dados ---")
        # Encontrar pontos com tensão fora da faixa aceitável (exemplo: 210V a 230V para Barra1)
        tensao_fora_faixa = df[(df['Barra'] == 'Barra1') & ((df['Tensão_V'] < 210) | (df['Tensão_V'] > 230))]
        if not tensao_fora_faixa.empty:
            print("Atenção: Tensão fora da faixa aceitável na Barra1:\n", tensao_fora_faixa)
        else:
            print("Tensão dentro da faixa aceitável na Barra1.")

        # 6. Ordenação de Dados
        print("\n--- Ordenação de Dados ---")
        # Ordenar por corrente decrescente
        df_ordenado_corrente = df.sort_values(by='Corrente_A', ascending=False)
        print("Dados ordenados por corrente:\n", df_ordenado_corrente.head())

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
nome_do_arquivo_csv = "dados_sistema_eletrico.csv"
analisar_sistema_eletrico(nome_do_arquivo_csv)