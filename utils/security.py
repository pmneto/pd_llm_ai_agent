import re

PALAVRAS_PROIBIDAS = [
    # Tentativas de prompt injection / manipulação
    "ignore o prompt", "haja como", "execute como", "as an AI", "you are now", 
    "system:", "you must obey", "disregard previous", "forget previous instructions", 
    "jailbreak", "bypass", "prompt injection"
]

def sanitizar_input(user_input: str) -> str:
    for palavra in PALAVRAS_PROIBIDAS:
        if re.search(rf"\b{re.escape(palavra)}\b", user_input, re.IGNORECASE):
            return "⚠️ Essa pergunta não pode ser respondida. Por favor, reformule."
    return user_input
