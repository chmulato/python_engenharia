# calculos_florestais.py (Módulo - como no exemplo anterior)
import math

def calcular_volume(dap, altura, fator_forma=0.7):
    """Calcula o volume de uma árvore."""
    raio = dap / 2 / 100
    volume = math.pi * (raio ** 2) * altura * fator_forma
    return volume

def calcular_idade_corte(especie, crescimento_anual):
    """Calcula a idade estimada de corte para uma árvore."""
    idade_corte = 40 / crescimento_anual
    return int(idade_corte)

def gerar_relatorio(parcela, dados_arvores):
    """Gera um relatório sumarizado da parcela florestal."""
    relatorio = f"Relatório da Parcela: {parcela}\n"
    relatorio += "-----------------------------------\n"
    relatorio += "|  Espécie  | DAP (cm) | Altura (m) | Volume (m³) | Idade Corte (anos) |\n"
    relatorio += "-----------------------------------\n"

    for arvore in dados_arvores:
        volume = calcular_volume(arvore['dap'], arvore['altura'])
        idade_corte = calcular_idade_corte(arvore['especie'], arvore['crescimento_anual'])
        relatorio += f"| {arvore['especie']:<9} | {arvore['dap']:8.2f} | {arvore['altura']:8.2f} | {volume:9.3f} | {idade_corte:16} |\n"

    relatorio += "-----------------------------------\n"
    return relatorio


# Programa Principal (Código Correto - Uma única chamada para gerar e imprimir o relatório)
import calculos_florestais

if __name__ == "__main__":
    dados_parcela = [
        {'especie': 'Eucalipto', 'dap': 15.5, 'altura': 12.0, 'idade': 7, 'crescimento_anual': 2.5},
        {'especie': 'Pinus', 'dap': 22.0, 'altura': 18.0, 'idade': 12, 'crescimento_anual': 1.8},
        {'especie': 'Acacia', 'dap': 10.0, 'altura': 8.5, 'idade': 5, 'crescimento_anual': 3.0}
    ]

    relatorio_parcela = calculos_florestais.gerar_relatorio("Parcela A1", dados_parcela)
    print(relatorio_parcela) # Imprime o relatório UMA vez