import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document


def load_docs(pasta_pdfs="data/pdfs"):
    """
    Loads all PDF documents from the specified folder using LangChain's PyPDFLoader.

    :param pasta_pdfs: Path to the folder containing PDF files.
    :return: A list of LangChain Document objects extracted from the PDFs.
    """
    documentos = []
    for nome_arquivo in os.listdir(pasta_pdfs):
        if nome_arquivo.endswith(".pdf"):
            caminho = os.path.join(pasta_pdfs, nome_arquivo)
            loader = PyPDFLoader(caminho)
            documentos.extend(loader.load())
    return documentos

def split_docs(documentos, chunk_size=1000, chunk_overlap=200):
    """
    Splits a list of Document objects into smaller chunks using a recursive text splitter.
    :param documentos: List of LangChain Document objects.
    :param chunk_size: Maximum number of characters per chunk.
    :param chunk_overlap: Number of characters that overlap between chunks.
    :return: A list of split Document objects, preserving metadata.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documentos)

def load_kaggle_csv():
    """
    Loads and merges two Kaggle CSV wine datasets, then converts each row into a LangChain Document object.

    :return: A list of Document objects, each containing a wine description and metadata
             such as country, winery, variety, points, and price.
    """
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