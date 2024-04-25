import requests
from bs4 import BeautifulSoup

r = requests.get('https://baomoi.com/tag/LITE.epi')

soup = BeautifulSoup(r.text, 'html.parser')

mydivs = soup.find_all("h3", {"class": "font-semibold block"})

for new in mydivs:
    print(new.a.get('title'))
    print(new.a.get('href'))