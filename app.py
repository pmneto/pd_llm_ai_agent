import os
import streamlit as st
from dotenv import load_dotenv
from utils.download_docs import baixar_pdfs
from rag.loader import load_docs, load_kaggle_csv
from rag.indexer import load_vector_index, create_index
from agents.wine_agent import build_agent
from utils.security import sanitizar_input

# Configura a página
st.set_page_config(page_title="CariocaWine", page_icon="🍷", layout="wide")
load_dotenv()

INDEX_PATH = "data/index_faiss"

def preparar_indice():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(os.path.join(INDEX_PATH, "index.faiss")):
        baixar_pdfs("data/docs")
        chunks = load_docs("data/docs")
        chunks_kaggle = load_kaggle_csv()
        create_index(chunks + chunks_kaggle)

def main():
    preparar_indice()

    if "historico" not in st.session_state:
        st.session_state.historico = []

    # Layout
    col_left, col_right = st.columns([4.5, 1.0], gap="small")

    with col_left:
        st.title("🍷 CariocaWine - IA Sommelier")

        # Formulário de pergunta
        pergunta = st.chat_input("Pergunte sobre vinhos, harmonizações ou onde comprar:")

        if pergunta:
            pergunta = sanitizar_input(pergunta)
            if pergunta.startswith("⚠️"):
                st.error(pergunta)
                return

            # Salva pergunta
            st.session_state.historico.append(("Usuário", pergunta))

            with st.spinner("Consultando o sommelier virtual..."):
                agente = build_agent()
                resposta = agente.invoke({"input": pergunta}).get("output", "Desculpe, não consegui gerar uma resposta.")

            # Salva resposta
            st.session_state.historico.append(("CariocaWine", resposta))

        # Renderiza histórico (sempre)
        for autor, mensagem in st.session_state.historico:
            with st.chat_message("user" if autor == "Usuário" else "assistant"):
                st.markdown(mensagem)

        # Ações
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🧹 Limpar conversa"):
                st.session_state.historico = []
        with col2:
            st.markdown("📸 Siga no Instagram: [@cariocawine](https://www.instagram.com/cariocawine)", unsafe_allow_html=True)

    with col_right:
        # Força o frame a colar na borda direita
        st.markdown("""
            <style>
                .element-container:has(iframe) {
                    padding-right: 0px !important;
                    margin-right: 0px !important;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("### 📷 Última postagem")
        st.components.v1.iframe(
            "https://www.instagram.com/p/C6YNzN4JwK6/embed",
            height=430,
            width=360,
            scrolling=True,
        )


if __name__ == "__main__":
    main()
