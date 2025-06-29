import os
import streamlit as st
from dotenv import load_dotenv
import datetime 

load_dotenv()

from utils.download_docs import baixar_pdfs
from rag.loader import load_docs, load_kaggle_csv, load_zonasul_documents
from rag.indexer import load_vector_index, create_index
from agents.wine_agent import build_agent
from utils.security import sanitizar_input
from utils.south_zone_extract import ZonaSulScraper



# Configura a página
st.set_page_config(page_title="CariocaWine", page_icon="🍷", layout="wide")

INDEX_PATH = "data/index_faiss"

def carregar_rag_zs():
      if not os.path.isfile("data/docs/vinhos.json"):
         zonasul = ZonaSulScraper()
         html = zonasul.buscar_html()
         vinhos = zonasul.extrair_vinhos_do_html(html)   
         zonasul.salvar_como_json()
      else:
         print("rag do zona sul já carregada.")
   


def preparar_indice():

    if not os.path.exists(INDEX_PATH) or not os.path.exists(os.path.join(INDEX_PATH, "index.faiss")):
        baixar_pdfs("data/docs")
        chunks = load_docs("data/docs")
        chunks_kaggle = load_kaggle_csv()
        chunks_zs = load_zonasul_documents("data/docs/vinhos.json")

        create_index(chunks + chunks_kaggle + chunks_zs)

def main():

    
        
      
        carregar_rag_zs()
        
        preparar_indice()


        
        if "historico" not in st.session_state:
            st.session_state.historico = []

        st.title("🍷 CariocaWine - IA Sommelier")
        st.markdown("### Descubra vinhos incríveis, sugestões de harmonização e onde comprar — tudo com a ajuda da IA mais carioca do pedaço! 🧠❤️🍇")



        # Renderiza histórico antes da entrada
        for autor, mensagem in st.session_state.historico:
            with st.chat_message("user" if autor == "Usuário" else "assistant"):
                st.markdown(mensagem)

        # Campo de pergunta
        pergunta = st.chat_input("Vai lá, pergunta qualquer coisa sobre vinhos! ;)")

        if pergunta:
            pergunta = sanitizar_input(pergunta)
            if pergunta.startswith("⚠️"):
                st.error(pergunta)
                return

            st.session_state.historico.append(("Usuário", pergunta))

            with st.spinner("Consultando o sommelier virtual..."):
                agente = build_agent()
                resposta = agente.invoke({"input": pergunta}).get("output", "Desculpe, não consegui gerar uma resposta.")
            
            
            resposta.replace("R$", "R\\$")
            st.session_state.historico.append(("CariocaWine", resposta))
            st.rerun()  # Força reposicionamento após nova mensagem

        # ✅ Área para os botões após input
        placeholder = st.empty()
        with placeholder.container():
            st.markdown("---")
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("✨ Iniciar outro chat"):
                    st.session_state.historico = []
                    st.rerun()
            with col2:
                st.markdown("📸 Siga no Instagram: [@cariocawine](https://www.instagram.com/cariocawine)", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
