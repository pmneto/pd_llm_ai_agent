import os
import requests

PDFS = {
    "Sommelier_Modulo_Basico.pdf": "https://dl.dropboxusercontent.com/scl/fi/q9vfdqx43iwueojh8jh1p/06.-Sommelier-M-dulo-B-sico-autor-Associa-o-Brasileira-de-Sommeliers-Paran.pdf?rlkey=tl92uwau10r6qz4wfd3fciqnz&amp;dl=0",
    "qualidade_na_producao_vinicola.pdf": "https://dl.dropboxusercontent.com/scl/fi/tuaokna44ogou5pmcgow6/05.-A-Qualidade-Na-Produ-o-Vin-cola-autor-Amanda-Cristina-Pereira-e-Thomas-Ribeiro.pdf?rlkey=wtztlwehe2kgj32lbjrvweonu&dl=0",
    "guia_pratico_do_vinho.pdf": "https://dl.dropboxusercontent.com/scl/fi/1tgk2ya57te1w06wubyrm/07.-Guia-Pr-tico-do-Vinho-autor-Lucas-Cordeiro.pdf?rlkey=hd71al1n1tsar6437vsd8x5ze&dl=0",
}



def baixar_pdfs(destino="data/pdfs"):
    os.makedirs(destino, exist_ok=True)
    
    for nome, url in PDFS.items():
        caminho_arquivo = os.path.join(destino, nome)
        if not os.path.exists(caminho_arquivo):
            print(f" Baixando {nome}...")
            resposta = requests.get(url)
            with open(caminho_arquivo, "wb") as f:
                f.write(resposta.content)
        else:
            print(f"{nome} já existe.")
