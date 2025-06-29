import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

class DuckDuckGoSearch:
    @staticmethod
    def extrair_conteudo(url, max_chars=700):
        """Scraps the website content"""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            textos = soup.stripped_strings
            texto = " ".join(textos)
            return texto[:max_chars] + "..." if len(texto) > max_chars else texto
        except Exception as e:
            return f"[Erro ao acessar {url[:50]}...]"

    @staticmethod
    def busca_duckduckgo(query: str) -> str:
        """Searches and format the query outcomes"""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            url = f"https://html.duckduckgo.com/html/?q={query}"
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")

            resultados = soup.find_all("a", class_="result__a", limit=5)
            if not resultados:
                return "Nenhum resultado encontrado."

            resposta = "🔎 Resultados da busca DuckDuckGo com contexto:\n\n"
            for i, r in enumerate(resultados[:5]):  # Limita para performance
                titulo = r.get_text(strip=True)
                raw_link = r.get("href", "").split('&rut=')[0]
                link_real = unquote(raw_link.split("uddg=")[-1]) if "uddg=" in raw_link else raw_link

                # Agora sim, aqui chamamos o raspador
                contexto = DuckDuckGoSearch.extrair_conteudo(link_real)

                resposta += f"{i+1}. [{titulo}]({link_real})\n📝 {contexto}\n\n"
                print(resposta)
                print("contexto: \n",contexto)
            return resposta

        except Exception as e:
            return f"❌ Erro ao buscar no DuckDuckGo: {e}"
