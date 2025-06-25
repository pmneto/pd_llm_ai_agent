# helpers/processar_pdfs.py

import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extrair_texto_pdfs(pasta="data/pdfs"):
    textos = {}
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".pdf"):
            caminho = os.path.join(pasta, nome_arquivo)
            leitor = PdfReader(caminho)
            texto_total = ""
            for pagina in leitor.pages:
                texto_total += pagina.extract_text() or ""
            textos[nome_arquivo] = texto_total
    return textos

def dividir_em_chunks(textos, tamanho=1000, sobreposicao=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=tamanho,
        chunk_overlap=sobreposicao
    )
    chunks = []
    for nome, texto in textos.items():
        partes = splitter.split_text(texto)
        for parte in partes:
            chunks.append({"origem": nome, "conteudo": parte})
    return chunks
