import requests
from bs4 import BeautifulSoup

url="https://www.edustoke.com/best-schools-in-india"
res=requests.get(url)
print(res)
data = (91,2,3)
type(data)
