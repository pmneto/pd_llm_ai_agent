import os
import requests
import zipfile
from io import BytesIO

PDFS = {
    "guia_pratico_do_vinho.pdf": "https://dl.dropboxusercontent.com/scl/fi/1tgk2ya57te1w06wubyrm/07.-Guia-Pr-tico-do-Vinho-autor-Lucas-Cordeiro.pdf?rlkey=hd71al1n1tsar6437vsd8x5ze&dl=0",
    "vinhos_sem_misterio.pdf": "https://dl.dropboxusercontent.com/scl/fi/r6749ha3sx0z5hd9pxn2y/Vinhos-sem-Misterio-Rafael-Roseira.pdf?rlkey=j9ostgruhxxtg6ybqcpezfe78&dl=0",
    "wine-reviews.zip": "https://www.kaggle.com/api/v1/datasets/download/zynicide/wine-reviews",
    "portuguese_wines.csv":"https://github.com/pazzolini/portuguese-wine-vivino/raw/7fed8a2a0107a124bc906ca0eb85f1fe7beda5c6/pt_wine_merged.csv"
}

# Arquivos esperados dentro do ZIP
WINE_FILES = {
    "winemag-data-130k-v2.csv",
    "winemag-data-130k-v2.json",
    "winemag-data_first150k.csv"
}

def baixar_pdfs(destino="data/docs"):
    os.makedirs(destino, exist_ok=True)

    for nome, url in PDFS.items():
        caminho_arquivo = os.path.join(destino, nome)

        # Lida com o ZIP separadamente
        if nome.endswith(".zip"):
            arquivos_faltando = [arq for arq in WINE_FILES if not os.path.exists(os.path.join(destino, arq))]
            if not arquivos_faltando:
                print("✅ Arquivos de wine já existem. Nenhum download necessário.")
                continue

            print("📦 Baixando e extraindo wine-reviews.zip...")
            response = requests.get(url)
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                z.extractall(destino)
                print("✅ Arquivos de wine extraídos com sucesso.")
        else:
            # Baixar PDFs normalmente
            if not os.path.exists(caminho_arquivo):
                print(f"📥 Baixando {nome}...")
                response = requests.get(url)
                with open(caminho_arquivo, "wb") as f:
                    f.write(response.content)
                print(f"✅ {nome} baixado.")
            else:
                print(f"✔️ {nome} já existe.")
