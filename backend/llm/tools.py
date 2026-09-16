import httpx
from bs4 import BeautifulSoup

async def web_search(query: str) -> str:
    """Realiza uma busca rápida na web usando o DuckDuckGo HTML."""
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data={"q": query}, headers=headers, timeout=10.0)
            if response.status_code != 200:
                return "Não consegui acessar a web agora."
            
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            
            for a in soup.find_all("a", class_="result__snippet", limit=3):
                results.append(a.get_text(strip=True))
                
            if not results:
                return "Nenhum resultado relevante encontrado."
                
            return "\n".join(results)
        except Exception as e:
            return f"Erro ao buscar na internet: {str(e)}"