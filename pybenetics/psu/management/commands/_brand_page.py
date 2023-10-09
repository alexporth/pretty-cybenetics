import requests
from bs4 import BeautifulSoup


class BrandPage:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        + "Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    tab_dictionary = {"efficiency": 1, "noise": 2}
    brand_urls = {}

    def __init__(self, tab: str):
        self.url = f"https://www.cybenetics.com/index.php?option=database&params=1,{self.tab_dictionary[tab]},0"

    def parse(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="mytable")

        for table_parts in table.find_all("tbody"):
            rows = table_parts.find_all("tr")
            for row in rows[1:]:
                row_header = row.find_all("th")
                if not row_header:
                    continue
                name = row_header[0].text
                if name in self.brand_urls:
                    continue
                url = row.find_all("a", href=True)[0].get("href").replace("¶", "&para")
                if not url.startswith("index"):
                    continue
                self.brand_urls[name] = url
