from duckduckgo_search import DuckDuckGoSearchRun

class DuckDuckGoSearch:
    def run(self, query: str) -> str:
        print(f"[DEBUG] Fazendo busca por: {query}")  # você pode usar logger se quiser
        search = DuckDuckGoSearchRun()
        results = search.run(query, max_results=5)
        return "\n".join(results) if results else "Não encontrei resultados relevantes no momento."
