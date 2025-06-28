import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

CAMINHO_INDEX = "data/index_faiss"

def create_index(chunks, caminho_index=CAMINHO_INDEX):
    """
    Creates a FAISS vector index from a list of document chunks.

    :param chunks: List of Document objects containing text and metadata.
    :param caminho_index: Path where the FAISS index will be saved locally.
    :return: FAISS object containing the vectorized index.
    """
    textos = [c.page_content for c in chunks]       
    metadados = [c.metadata for c in chunks]        

    embeddings = OpenAIEmbeddings()
    index = FAISS.from_texts(textos, embedding=embeddings, metadatas=metadados)

    index.save_local(caminho_index)
    print(f"Índice vetorial salvo em: {caminho_index}")

    return index

def load_vector_index(caminho_index=CAMINHO_INDEX):
    """
    Loads a previously saved FAISS vector index from local storage.

    :param caminho_index: Path to the directory containing the FAISS index.
    :return: FAISS object with the loaded index ready for search.
    :raises FileNotFoundError: If the index directory does not exist.
    """
    if not os.path.exists(caminho_index):
        raise FileNotFoundError(f"Caminho não encontrado: {caminho_index}")

    embeddings = OpenAIEmbeddings()
    index = FAISS.load_local(caminho_index, embeddings, allow_dangerous_deserialization=True)
    print(f"Índice vetorial carregado de: {caminho_index}")

    return index

def create_zonasul_index(documentos, caminho_index="data/index_vinhos"):
    embeddings = OpenAIEmbeddings()
    index = FAISS.from_documents(documentos, embedding=embeddings)
    index.save_local(caminho_index)
    print(f"🔎 Índice vetorial salvo em {caminho_index}")
    return index