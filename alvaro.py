import requests
import tempfile
import pdfplumber
import re

# URL do PDF
pdf_url = "https://www.cfn.org.br/wp-content/uploads/2017/03/taco_4_edicao_ampliada_e_revisada.pdf"

# Baixar o PDF da web
response = requests.get(pdf_url)
response.raise_for_status()

# Salvar temporariamente
with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
    tmp_file.write(response.content)
    temp_pdf_path = tmp_file.name

# Inicializar lista para armazenar os dados da Tabela 1
tabela_1_dados = []

# Ler o PDF e extrair dados da Tabela 1
with pdfplumber.open(temp_pdf_path) as pdf:
    for page in pdf.pages:
        texto = page.extract_text()
        if texto and "Tabela 1. Composição de alimentos por 100 gramas de parte comestível" in texto:
            linhas = texto.split("\n")
            for linha in linhas:
                # Ignorar cabeçalhos e linhas irrelevantes
                if re.search(r"\d", linha) and not linha.startswith("Tabela"):
                    partes = linha.split()
                    
                    if len(partes) >= 11:
                        
                        nome_alimento = str(partes[1:-11])
                        energia = partes[-10]
                        proteina = partes[-8]
                        lipideos = partes[-7]
                        #print(nome_alimento)
                        # Excluir nomes que contenham apenas números ou comecem com números
                        if not re.fullmatch(r"[\d,.]+", nome_alimento):
                            tabela_1_dados.append((nome_alimento, energia, proteina, lipideos))

# Exibir os dados extraídos
for alimento in tabela_1_dados:
    print(f"Alimento: {alimento[0]}, Energia: {alimento[1]}, Proteína: {alimento[2]}, Lipídeos: {alimento[3]}")