import asyncio
import aiohttp
import time
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
# from random import choice


# для асинхронной записи нужно использовать доп библиотеки "qrio","aiofiles"
ua = UserAgent()
start_time = time.time()


async def get_page_data(session, page):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": f"{ua.random}"
    }

    url = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={page}&region=1&room1=1&room2=1#"

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "lxml")
        try:
            for a in soup.find("div", attrs={"data-name": "Offers"}).find_all("a", class_=re.compile("--link--eoxce")):
                print("{} ,{}".format(a.get("href"), page))
        except Exception as ex:
            print(ex)
        try:
            # Suggestions
            for a in soup.find("div", attrs={"data-name": "Suggestions"}).find_all("a", class_=re.compile("--link--eoxce")):
                print("new {}".format(a.get("href")))
        except Exception as ex:
                pass

async def gather_data():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": f"{ua.random}"
    }

    url = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=1&room1=1&room2=1"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        # page_count = int(soup.find("div", attrs={"data-name": "Pagination"}).find_all("li")[-2].text)

        page_count = 54

        tasks = []

        for page in range(1, page_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())
    print(f"54 page {time.time() - start_time} second")


if __name__ == "__main__":
    main()

# https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=54&region=1&room1=1&room2=1&room3=1
# https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=54&region=1&room1=1&room2=1&room3=1#
# response.json()
# реализовать постоянную подгрузку с проверкой на схожость