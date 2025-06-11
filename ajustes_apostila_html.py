"""
ajustes_apostila_html.py

Este script automatiza ajustes em arquivos HTML gerados a partir da apostila de Python para Engenharia.
Principais funções:
- Gera automaticamente um sumário navegável (topdown) com base nos títulos (h1-h6) do documento.
- Insere estilos CSS para visual moderno e alinhamento centralizado do conteúdo.
- Adiciona um botão "⬆️ Sumário" após cada seção/título, facilitando a navegação do leitor.
- Remove estilos antigos e garante que o novo CSS seja aplicado corretamente.
- Salva o HTML ajustado em um novo arquivo de saída.

Uso:
    Execute este script no mesmo diretório do arquivo HTML de entrada.
    O arquivo ajustado será salvo como 'python_engenharia_ajustado_final.html'.

Requisitos:
    - BeautifulSoup4 (bs4)
    - Python 3.x

Autor: Christian Vladimir Uhdre Mulato
Apoio: Develcode – Consultoria em Tecnologia
"""
from bs4 import BeautifulSoup
import os

# --- CSSs usados ---
CSS_SUMARIO = """
<style>
nav {
    background: #f8f9fa;
    padding: 24px 20px 20px 20px;
    border-radius: 10px;
    margin-bottom: 32px;
    border: 1px solid #dee2e6;
    max-width: 600px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
nav h3 {
    color: #007bff;
    margin-bottom: 18px;
    border-bottom: 2px solid #007bff22;
    padding-bottom: 6px;
    font-size: 1.3em;
    font-weight: 600;
}
nav ol, nav ul {
    padding-left: 20px;
    line-height: 1.7;
}
nav li {
    margin-bottom: 6px;
}
nav a {
    text-decoration: none;
    color: #007bff;
    font-weight: 500;
    transition: color 0.2s;
}
nav a:hover {
    color: #0056b3;
    text-decoration: underline;
}
html {
    scroll-behavior: smooth;
}
:target {
    background: #fff3cd;
    padding: 8px;
    border-radius: 5px;
    border-left: 4px solid #ffc107;
    margin: 10px 0;
}
</style>
"""

CSS_ALINHAMENTO = """
<style>
body {
    max-width: 760px;
    margin: 0 auto !important;
    padding: 24px 12px 32px 12px;
    font-size: 1.08em;
    line-height: 1.7;
    background: #fff;
}
figure, nav, h1, h2, h3, h4, h5, h6, p, ul, ol, pre, table, blockquote {
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}
p {
    text-align: justify;
}
</style>
"""

BOTAO_SUMARIO = '''
<a href="#sumário" class="btn-voltar-sumario" style="
    display:inline-block;
    margin:6px 0 18px 0;
    padding:2px 8px;
    background:none;
    color:#007bff !important;
    border-radius:4px;
    font-size:0.97em;
    text-decoration:underline;
    font-weight:400;
    box-shadow:none;
    border:none;
    opacity:0.7;
    transition:opacity 0.2s;
">⬆️ Sumário</a>
'''

IGNORAR_IDS = {'sumário', 'título-introdução-à-programação-python-aplicada-à-engenharia', 'autor-christian-vladimir-uhdre-mulato'}

def gerar_novo_sumario(soup):
    titulos = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], attrs={'id': True})
    titulos_validos = [t for t in titulos if t['id'] not in IGNORAR_IDS]
    sumario_html = []
    nivel_atual = 0
    pilha = []

    for titulo in titulos_validos:
        nivel = int(titulo.name[1])
        texto = titulo.get_text().strip()
        id_titulo = titulo['id']
        item = f'<li><a href="#{id_titulo}">{texto}</a>'

        if nivel > nivel_atual:
            sumario_html.append('<ol>' * (nivel - nivel_atual))
            pilha.extend([nivel] * (nivel - nivel_atual))
        elif nivel < nivel_atual:
            sumario_html.append('</li>' + '</ol></li>' * (nivel_atual - nivel))
            for _ in range(nivel_atual - nivel):
                if pilha: pilha.pop()
        else:
            sumario_html.append('</li>')

        sumario_html.append(item)
        nivel_atual = nivel

    while nivel_atual > 0:
        sumario_html.append('</li></ol>')
        nivel_atual -= 1

    novo_sumario = '<nav>\n<h3 id="sumário">Sumário</h3>\n<ol type="1">\n' + '\n'.join(sumario_html) + '\n</ol>\n</nav>'
    sumario_section = soup.find('h3', {'id': 'sumário'})
    if sumario_section:
        ol = sumario_section.find_next('ol')
        if ol:
            ol.replace_with(BeautifulSoup(novo_sumario, 'html.parser'))
    return soup

def inserir_css_sumario_e_alinhamento(soup):
    # Garante que existe <head>
    if soup.head is None:
        head_tag = soup.new_tag('head')
        if soup.html:
            soup.html.insert(0, head_tag)
        else:
            soup.insert(0, head_tag)
    else:
        head_tag = soup.head

    # Remove todos os <style> antigos
    for style in head_tag.find_all('style'):
        style.decompose()

    # Adiciona ambos os CSS
    head_tag.append(BeautifulSoup(CSS_SUMARIO, 'html.parser'))
    head_tag.append(BeautifulSoup(CSS_ALINHAMENTO, 'html.parser'))
    return soup

def inserir_botoes_sumario(soup):
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], id=True):
        if tag['id'] not in IGNORAR_IDS:
            proximo = tag.find_next_sibling()
            if not (proximo and getattr(proximo, 'get', lambda x: None)('class') == ['btn-voltar-sumario']):
                tag.insert_after(BeautifulSoup(BOTAO_SUMARIO, 'html.parser'))
    return soup

def pipeline_ajustes(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    soup = gerar_novo_sumario(soup)
    soup = inserir_css_sumario_e_alinhamento(soup)
    soup = inserir_botoes_sumario(soup)

    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"Arquivo final salvo como '{arquivo_saida}'.")

if __name__ == "__main__":
    entrada = "python_engenharia.html"
    saida = "python_engenharia_ajustado_final.html"
    if os.path.exists(entrada):
        pipeline_ajustes(entrada, saida)
    else:
        print(f"Arquivo {entrada} não encontrado.")