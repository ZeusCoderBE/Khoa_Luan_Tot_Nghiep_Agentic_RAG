import requests
from typing import List
from source.core.config import Settings
import requests
from bs4 import BeautifulSoup
from typing import List
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from typing import List
from selenium import webdriver
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
    def extract_text_from_url(self, link: str) -> str:
        content = ""
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )

        driver = webdriver.Edge(options=edge_options)
        try:
            # Ưu tiên dùng Selenium để đảm bảo lấy được nội dung động
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            content = soup.get_text(separator="\n", strip=True)
        except Exception as e:
            print(f"Lỗi khi truy cập link {link}: {e}")
        finally:
            driver.quit()

        return content or "[Empty Content]"

    def extract_texts_from_links(self, links: List[str]) -> List[str]:
        return [self.extract_text_from_url(url) for url in links]

