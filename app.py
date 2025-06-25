import os
import streamlit as st
from dotenv import load_dotenv

# ✅ Primeira chamada obrigatória!
st.set_page_config(page_title="CariocaWine", page_icon="🍷")
load_dotenv()

from utils.download_docs import baixar_pdfs
from rag.loader import load_docs, load_kaggle_csv
from rag.indexer import load_vector_index, create_index
from agents.wine_agent import build_agent

INDEX_PATH = "data/index_faiss"

def preparar_indice():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(os.path.join(INDEX_PATH, "index.faiss")):
        st.warning("📦 Índice vetorial não encontrado. Preparando ambiente...")
        baixar_pdfs("data/docs")
        chunks = load_docs("data/docs")
        chunks_kaggle = load_kaggle_csv()
        create_index(chunks + chunks_kaggle)
        st.success("✅ PDFs baixados e índice criado com sucesso!")
    else:
        st.info("🧠 Índice encontrado. Pronto para uso!")

def main():
    preparar_indice()

    st.title("🍷 CariocaWine - Seu Sommelier Digital")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(""" ---
        🧹 Limpar conversa"""):
            st.session_state.historico = []

    with col2:
        st.markdown(
             """
    ---
    📸 Nos siga no Instagram: [@cariocawine](https://www.instagram.com/cariocawine)
    """,
            unsafe_allow_html=True
        )

    # Histórico
    if "historico" not in st.session_state:
        st.session_state.historico = []

    pergunta = st.text_input("O que deseja saber sobre vinhos, harmonizações ou onde comprar?")

    if pergunta:
        with st.spinner("Consultando o sommelier virtual..."):
            agente = build_agent()
            resposta = agente.invoke({"input": pergunta})["output"]

        st.session_state.historico.append(("Usuário", pergunta))
        st.session_state.historico.append(("CariocaWine", resposta))

    for autor, mensagem in st.session_state.historico:
        with st.chat_message("user" if autor == "Usuário" else "assistant"):
            st.markdown(mensagem)

if __name__ == "__main__":
    main()
