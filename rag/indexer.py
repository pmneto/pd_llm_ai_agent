import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

CAMINHO_INDEX = "data/index_faiss"

def create_index(chunks, caminho_index=CAMINHO_INDEX):
    textos = [c.page_content for c in chunks]       # 👈 correto
    metadados = [c.metadata for c in chunks]        # 👈 correto

    embeddings = OpenAIEmbeddings()
    index = FAISS.from_texts(textos, embedding=embeddings, metadatas=metadados)

    index.save_local(caminho_index)
    print(f"✅ Índice vetorial salvo em: {caminho_index}")

    return index

def load_vector_index(caminho_index=CAMINHO_INDEX):
    if not os.path.exists(caminho_index):
        raise FileNotFoundError(f"❌ Caminho não encontrado: {caminho_index}")

    embeddings = OpenAIEmbeddings()
    index = FAISS.load_local(caminho_index, embeddings, allow_dangerous_deserialization=True)
    print(f"📦 Índice vetorial carregado de: {caminho_index}")

    return index
