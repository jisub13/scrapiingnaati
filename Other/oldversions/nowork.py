import requests
import urllib.request
from bs4 import BeautifulSoup
import time;
import pyperclip
url = "https://www.naati.com.au/online-directory/?require=interpreter&for=[482,570,707,724,1306,1487,1551,1277,1300]"
source = requests.get(url)
soup = BeautifulSoup(source.content, 'html5lib')
print(soup)
l = soup.find_all("a", attrs={"data-personid":True})
print(l)
