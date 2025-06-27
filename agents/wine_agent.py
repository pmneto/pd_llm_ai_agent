from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from rag.searcher import search_context
from rag.indexer import load_vector_index  # Supondo que exista para carregar FAISS/Chroma
from tools.weather_tool import consultar_clima
from langchain.memory import ConversationBufferMemory
from tools.search_tool import DuckDuckGoSearch
from tools.getday import get_today


search = DuckDuckGoSearch()

# Carrega o índice vetorial para uso no RAG
index = load_vector_index()

# Estabelece uma "Memória" para o chat
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def carregar_prompt_base(caminho="./prompts/prompt_base.md"):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

# Função apenas com RAG
def consultar_contexto(pergunta: str) -> str:
    """Query using only RAG (Retrieval-Augmented Generation)."""
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
        description="Use this tool to answer questions about wine using relevant documents as context. Ideal for specialized wine knowledge."
    ),
    Tool(
        name="ClimaAtual",
        func=consultar_clima,
        description="Use this tool to fetch the current local weather based on the user's IP. Useful when weather may influence wine choices or outdoor events."
    ),
    Tool(
        name="DuckDuckgoPesquisa",
        func=search.busca_duckduckgo,
        description="Use this tool to perform real-time internet searches. Ideal when you need to fetch updated or external information not present in the documents."
    ),
    Tool(
        name="DiaAtual",
        func=get_today,
        description="Use this tool to know which day is today. Ideal when you need referrence."
    )
]


# Prompt com placeholders esperados
prompt = ChatPromptTemplate.from_messages([
    ("system", carregar_prompt_base()),
     MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
    
])

# Modelo
llm = ChatOpenAI(temperature=0.6)

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
    memory=memory,
    verbose=True,
    return_only_outputs=True,
    output_keys=["output"]
)