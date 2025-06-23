import streamlit as st
from utils.agent import build_agent

st.set_page_config(page_title="CariocaWine - SommelierGPT", layout="centered")

st.title("🍷 CariocaWine - SommelierGPT")
st.markdown("Fala comigo! Manda tua pergunta sobre vinho, harmonização, tipos de uva ou qualquer curiosidade enológica com o jeitinho carioca.")

# Cria o agente
agent = build_agent()

# Caixa de input
user_input = st.text_input("Digite sua pergunta:")

if st.button("Perguntar") and user_input:
    resposta = agent.run(
        f"Você é o SommelierGPT, um especialista em vinhos, leve, informal e carioca. Responda com simpatia e conhecimento. Pergunta: {user_input}"
    )
    st.markdown("### 🍇 Resposta do SommelierGPT:")
    st.write(resposta)
