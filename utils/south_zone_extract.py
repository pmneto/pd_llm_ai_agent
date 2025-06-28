import requests
from bs4 import BeautifulSoup
import json
import csv
import os
from typing import List, Dict


class ZonaSulScraper:
    def __init__(self, url: str = "https://www.zonasul.com.br/vinho", salvar_em: str = "data/docs"):
        # Garante que salvar_em seja uma string
        if isinstance(salvar_em, list):
            salvar_em = salvar_em[0]
        self.url = url
        self.salvar_em = salvar_em.rstrip("/")  # Remove barra final se houver
        self.vinhos: List[Dict] = []

    def buscar_html(self) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self.url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text

    def extrair_vinhos_do_html(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, "html.parser")
        tag_json = soup.find("script", {"type": "application/ld+json"})
        if not tag_json:
            raise ValueError("❌ Script JSON-LD não encontrado no HTML.")
        dados = json.loads(tag_json.string)

        vinhos_extraidos = []
        for item in dados.get("itemListElement", []):
            produto = item.get("item", {})
            vinho = {
                "nome": produto.get("name"),
                "descricao": produto.get("description", "").replace("&lt;br/&gt;", "\n"),
                "preco": produto.get("offers", {}).get("lowPrice"),
                "url": produto.get("@id"),
                "imagem": produto.get("image"),
                "marca": produto.get("brand", {}).get("name"),
            }
            vinhos_extraidos.append(vinho)

        self.vinhos = vinhos_extraidos
        return vinhos_extraidos

    def salvar_como_json(self, nome_arquivo="vinhos.json"):
        os.makedirs(self.salvar_em, exist_ok=True)
        caminho = os.path.join(self.salvar_em, nome_arquivo)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(self.vinhos, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON salvo em: {caminho}")

    def salvar_como_csv(self, nome_arquivo="vinhos.csv"):
        os.makedirs(self.salvar_em, exist_ok=True)
        caminho = os.path.join(self.salvar_em, nome_arquivo)
        if not self.vinhos:
            print("⚠️ Nenhum vinho para salvar.")
            return
        with open(caminho, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.vinhos[0].keys())
            writer.writeheader()
            writer.writerows(self.vinhos)
        print(f"✅ CSV salvo em: {caminho}")
