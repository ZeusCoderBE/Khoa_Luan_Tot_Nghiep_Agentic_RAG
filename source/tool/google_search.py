import requests
from typing import List
from source.core.config import Settings
import requests
from bs4 import BeautifulSoup
from typing import List
class GoogleSearchTool:
    def __init__(self,setting:Settings):
        self.api_key = setting.GOOGLE_SEARCH_API
        self.cse_id = setting.TOOL_SEARCH

    def search(self, query: str, num_results: int = 5) -> List[str]:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "key": self.api_key,
            "cx": self.cse_id,
            "num": num_results
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Search failed: {response.text}")
        results = response.json()
        links = []
        for item in results.get("items", []):
            links.append(item["link"])
        return links
    def extract_text_from_url(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10, verify=False)  # Tắt SSL verify
            if response.status_code != 200:
                return f"[Failed to fetch: {url}]"
            soup = BeautifulSoup(response.text, 'html.parser')
            for script_or_style in soup(["script", "style"]):
                script_or_style.extract()
            text = soup.get_text(separator=' ', strip=True)
            return text
        except requests.exceptions.SSLError as ssl_err:
            return f"[SSL Error fetching {url}]: {str(ssl_err)}"
        except Exception as e:
            return f"[Error fetching {url}]: {str(e)}"

    def extract_texts_from_links(self, links: List[str]) -> List[str]:
        texts = []
        for url in links:
            text = self.extract_text_from_url(url)
            texts.append(text)
        return texts    