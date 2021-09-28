import requests
from bs4 import BeautifulSoup

url = "https://www.palabrasaleatorias.com/random-words.php"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
block = soup.find_all("div")[1]#get second div
x = str(block.text.strip()))
