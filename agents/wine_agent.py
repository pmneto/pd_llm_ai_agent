from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from rag.searcher import search_context
from rag.indexer import load_vector_index  # Supondo que exista para carregar FAISS/Chroma

# Carrega o índice vetorial para uso no RAG
index = load_vector_index()

# Função apenas com RAG
def consultar_contexto(pergunta: str) -> str:
    """Consulta usando apenas o RAG."""
    contexto = search_context(pergunta, index=index)

    if contexto.strip():
        return f"Contexto dos documentos:{contexto}"
    else:
        return "Desculpe, não encontrei informações relevantes disponíveis."

# Ferramenta baseada apenas no RAG
tools = [
    Tool(
        name="BuscaContextualizada",
        func=consultar_contexto,
        description="Use para responder dúvidas sobre vinhos com base em contexto especializado nos documentos."
    )
]

# Prompt com placeholders esperados
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um sommelier digital. Ajude com perguntas sobre vinhos, harmonizações e onde comprar."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Modelo
llm = ChatOpenAI(temperature=0.7)

# Agente com funções
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)




def build_agent():
    from utils.download_docs import baixar_pdfs
    baixar_pdfs()
    return wine_search_chain


# Executor com retorno limpo
wine_search_chain = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_only_outputs=True,
    output_keys=["output"]
)