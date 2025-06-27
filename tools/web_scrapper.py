import requests
from bs4 import BeautifulSoup
import re

def scrappe_url(url: str) -> str:
    '''Scrappes a URL based on the prompt passed'''
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)

        if not resp.ok:
            return "❌ Não consegui acessar o site, irmão."

        soup = BeautifulSoup(resp.content, "html.parser")

        titulo = soup.title.string if soup.title else "Sem título"

        # Coleta os textos de h1, h2, h3 e p
        headers = soup.find_all(re.compile("^h[1-6]$"))
        paragrafos = soup.find_all("p")

        # Limita o total de blocos coletados para evitar texto excessivo
        headers_text = "\n".join(h.get_text(strip=True) for h in headers[:5])  # até 5 headers
        paragrafos_text = "\n".join(p.get_text(strip=True) for p in paragrafos[:10])  # até 10 parágrafos

        return f"📰 Título: {titulo}\n\n📌 Destaques:\n{headers_text}\n\n📄 Conteúdo:\n{paragrafos_text}"

    except Exception as e:
        return f"❌ Deu ruim ao raspar o site: {e}"
