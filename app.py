import os
import streamlit as st
from dotenv import load_dotenv

# ✅ DEVE SER A PRIMEIRA CHAMADA STREAMLIT!
st.set_page_config(page_title="CariocaWine", page_icon="🍷")

load_dotenv()

from utils.download_docs import baixar_pdfs
from rag.loader import load_docs
from rag.indexer import load_vector_index, create_index
from agents.wine_agent import build_agent  # já pode vir aqui mesmo

INDEX_PATH = "data/index_faiss"

def preparar_indice():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(os.path.join(INDEX_PATH, "index.faiss")):
        st.warning("📦 Índice vetorial não encontrado. Preparando ambiente...")
        baixar_pdfs("data/docs")
        chunks = load_docs("data/docs")
        create_index(chunks)
        st.success("✅ PDFs baixados e índice criado com sucesso!")
    else:
        st.info("🧠 Índice encontrado. Pronto para uso!")

def main():
    preparar_indice()

    st.title("🍷 CariocaWine - Seu Sommelier Digital")
    query = st.text_input("O que deseja saber sobre vinhos, harmonizações ou onde comprar?")

    if query:
        with st.spinner("Consultando o sommelier virtual..."):
            agent = build_agent()
            resposta = agent.invoke({"input": query})
        st.success("Resultado:")
        st.write(resposta)

if __name__ == "__main__":
    main()
