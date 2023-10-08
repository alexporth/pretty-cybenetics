import requests
from bs4 import BeautifulSoup


class BrandPage:
    tab_dictionary = {"efficiency": 1, "noise": 2}

    def __init__(self, tab: str):
        self.url = f"https://www.cybenetics.com/index.php?option=database&params=1,{self.tab_dictionary[tab]},0"

    def parse(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", id="mytable", class_="mytable")
        print()
