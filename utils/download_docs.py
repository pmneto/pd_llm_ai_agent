import os
import requests
import zipfile
from io import BytesIO

PDFS = {
    "guia_pratico_do_vinho.pdf": "https://dl.dropboxusercontent.com/scl/fi/1tgk2ya57te1w06wubyrm/07.-Guia-Pr-tico-do-Vinho-autor-Lucas-Cordeiro.pdf?rlkey=hd71al1n1tsar6437vsd8x5ze&dl=0",
    "vinhos_sem_misterio.pdf": "https://dl.dropboxusercontent.com/scl/fi/r6749ha3sx0z5hd9pxn2y/Vinhos-sem-Misterio-Rafael-Roseira.pdf?rlkey=j9ostgruhxxtg6ybqcpezfe78&dl=0",
    "guia_do_rio.pdf":"https://riotur.rio/wp-content/uploads/2024/08/Riotur_VisitRio_PocketGuide_85x125mm_miolo_SpecialEdition_BAIXA-4.pdf",
    "wine-reviews.zip": "https://www.kaggle.com/api/v1/datasets/download/zynicide/wine-reviews"

}  



def baixar_pdfs(destino="data/docs"):
    os.makedirs(destino, exist_ok=True)

    for nome, url in PDFS.items():
        caminho_arquivo = os.path.join(destino, nome)
        if not os.path.exists(caminho_arquivo):
            print(f" Baixando {nome}...")

            response = requests.get(url)
            if "zip" in nome:
                with zipfile.ZipFile(BytesIO(response.content)) as z:
                    z.extractall(destino)
                    print(f"Arquivo {nome} extraído.")
            else:
                with open(caminho_arquivo, "wb") as f:
                    f.write(response.content)
        else:
            print(f" {nome} já existe.")