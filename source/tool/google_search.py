import requests
from typing import List
from source.core.config import Settings
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
