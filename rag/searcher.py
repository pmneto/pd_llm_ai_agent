from langchain.vectorstores.base import VectorStore
from typing import Union, List
from langchain.schema import Document



def search_context(pergunta: str, index: Union[VectorStore, any], k: int = 3) -> str:
    """
    Runs a vector search on the index and returns a nicely formatted context.

    :param pergunta: The user's question.
    :param index: The vector index object (e.g., FAISS, Chroma).
    :param k: Number of top similar documents to fetch.
    :return: Combined text with the most relevant snippets.
    """

    if not pergunta or not index:
        return ""

    try:
        docs: List[Document] = index.similarity_search(pergunta, k=k)
        contexto = "\n\n".join([doc.page_content for doc in docs])
        return contexto
    except Exception as e:
        print(f"[Erro na busca vetorial]: {e}")
        return "Não foi possível buscar contexto adicional."
