# 🍷 CariocaWine AI - Virtual Sommelier do Rio

Bem-vindo ao **CariocaWine AI**, um agente inteligente feito com ❤️ no Rio de Janeiro. Ele funciona como um sommelier virtual com o jeitinho carioca, pronto para recomendar vinhos, harmonizações e informações sazonais de forma contextual, charmosa e divertida.

**Motivação: Projeto de Disciplina - IA generativa para linguagem (Large Language Model)**


---

## 🔎 Sobre o Projeto

Este projeto usa:

- [LangChain](https://www.langchain.com/) para orquestração do agente
- [FAISS](https://github.com/facebookresearch/faiss) + RAG (Retrieval-Augmented Generation)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Streamlit](https://streamlit.io/) para a interface
- Múltiplas ferramentas (plugins) como:
  - Clima local
  - Estação do ano
  - Scraping de URLs
  - Buscador com DuckDuckGo
  - Análise de vídeos do YouTube

- **Modelo LLM:** [`gpt-3.5-turbo`](https://platform.openai.com/docs/models/gpt-3-5) da OpenAI, utilizado via `langchain.chat_models.ChatOpenAI`



---


## 🚀 Como rodar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/agent-wine.git
cd agent-wine
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate   # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
```

3. Adicione um arquivo `.env` com suas credenciais da OpenAI (e outras, se necessário):

```env
OPENAI_API_KEY=sua-chave-aqui
```

4. Rode a aplicação:

```bash
streamlit run app.py
```

---

## 🧠 Arquitetura

```
.
├── app.py                 # Streamlit frontend
├── agents/               # Definições do agente LangChain
├── rag/                  # Indexação e busca com FAISS
├── tools/                # Ferramentas auxiliares (clima, estação, scraping, etc)
├── prompts/              # Prompt base do agente
├── data/index_faiss/     # Índice vetorial
├── requirements.txt
├── .env
└── README.md
```

---

## 🛡️ Segurança e Estilo

- O agente **recusa interações ofensivas ou fora do contexto de vinhos**.
- As respostas seguem um tom **leve, descontraído e carismático**, usando expressões típicas do carioca.

---

## 📌 Futuras melhorias

- Cache de buscas com SQLite
- Suporte a imagens de rótulos
- Integração com marketplaces e geolocalização real
- Exibição de ofertas
- Transição para arquitetura de backend e front-end mais robusta

---

## 🍷 Brinde final

Esse projeto é uma celebração da cultura do vinho, do jeito leve do Rio, e da tecnologia moderna.  
**Partiu tomar aquele brinde com estilo?**