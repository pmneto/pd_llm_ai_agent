from langchain.vectorstores.base import VectorStore
from typing import Union, List
from langchain.schema import Document



def search_context(pergunta: str, index: Union[VectorStore, any], k: int = 3) -> str:
    """
    Realiza uma busca vetorial no índice e retorna um contexto formatado.

    :param pergunta: Pergunta do usuário.
    :param index: Objeto do índice vetorial (FAISS, Chroma, etc).
    :param k: Número de documentos mais similares a retornar.
    :return: Texto concatenado com os trechos mais relevantes.
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
