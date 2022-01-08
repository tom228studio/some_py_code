import requests
from bs4 import BeautifulSoup
import json
import re
import asyncio
import aiohttp
import datetime

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36"
}

url = "https://streaminside.ru/posts"

req = requests.get(url, headers=headers)
src = req.text

with open("index.html", "a", encoding="UTF-8-sig") as file:
    file.write(src)

soup = BeautifulSoup(src, "lxml")
all_news = soup.find(id="posts_block").find_all("a")
all_useless = soup.find(id="posts_block").find_all("a", href=re.compile("/posts/"))
all_useless += soup.find(id="posts_block").find_all("a", href=re.compile("/vk/"))
all_useless += soup.find(id="posts_block").find_all("a", href=re.compile("/admin/"))

all_useless_list = ["javascript:void(0);"]
for item in all_useless:
    all_useless = item.get("href")
    all_useless_list.append(all_useless)

all_news_dict = {}
for item in all_news:
    item_text = item.text
    item_href = item.get("href")
    if item_href in all_useless_list:
        continue
    else:
        all_news_dict[item_text] = item_href

with open("new_news.json", "a", encoding="UTF-8-sig") as file:
    json.dump(all_news_dict, file, indent=4, ensure_ascii=False)
