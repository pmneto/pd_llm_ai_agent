import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document


def load_docs(pasta_pdfs="data/pdfs"):
    documentos = []
    for nome_arquivo in os.listdir(pasta_pdfs):
        if nome_arquivo.endswith(".pdf"):
            caminho = os.path.join(pasta_pdfs, nome_arquivo)
            loader = PyPDFLoader(caminho)
            documentos.extend(loader.load())
    return documentos

def split_docs(documentos, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documentos)

def load_kaggle_csv():
    caminho="data/docs/winemag-data_first150k.csv"
    caminho2="data/docs/winemag-data-130k-v2.csv"
    df = pd.read_csv(caminho)
    df2 = pd.read_csv(caminho2)

    df = pd.merge(df, df2, how = 'outer')
    documentos = []
    for _, row in df.iterrows():
        conteudo = f"{row.get('title', '')} - {row.get('description', '')}"
        metadados = {
            "pais": row.get("country"),
            "vinicola": row.get("winery"),
            "variedade": row.get("variety"),
            "pontos": row.get("points"),
            "preco": row.get("price")
        }
        documentos.append(Document(page_content=conteudo, metadata=metadados))
    return documentos