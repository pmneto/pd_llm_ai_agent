from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os

load_dotenv()

def build_agent():
    openai_key = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        openai_api_key=openai_key,
        model_name="gpt-3.5-turbo",
        temperature=0.7
    )

    memory = ConversationBufferMemory()
    return ConversationChain(llm=llm, memory=memory)
