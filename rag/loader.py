import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


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
