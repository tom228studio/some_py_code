import asyncio
import aiohttp
import time
import re
import psycopg2
# import pickle
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import choice
from config import host, user, password, db_name

# для асинхронной записи нужно использовать доп библиотеки "qrio","aiofiles"
ua = UserAgent()
start_time = time.time()
proxy = open("proxy").read().split('\n')

# try:
#     # config for connect
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=db_name
#     )
#     connection.autocommit = True
#
#     # db version for ping
#     with connection.cursor() as cursor:
#         cursor.execute(
#             "SELECT version();"
#         )
#         print(f"Server ver.:{cursor.fetchone()}")
#
#
#
# except Exception as ex_:
#     print(ex_)
# finally:
#
#     # check if its work close connection
#     if connection:
#         connection.close()
#         print("db closed")

async def get_page_data(session, page):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": f"{ua.random}"
    }

    url = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={page}&region=1&room1=1&room2=1"

    async with session.get(url=url, headers=headers, proxy=f"http://g8BapX:NHJ5bk@{choice(proxy)}") as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")

        try:
            for a in soup.find("div", attrs={"data-name": "Offers"}).find_all("a", class_=re.compile("--link--eoxce")):
                print("{} ,{}".format(a.get("href"), page))
        except Exception as ex:
            print(ex)


async def extra_page(session):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": f"{ua.random}"
    }
    url = "https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=54&region=1&room1=1&room2=1#"#ссылка на доп инфу

    async with session.get(url=url, headers=headers, proxy=f"http://g8BapX:NHJ5bk@{choice(proxy)}") as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")

        try:
            for a in soup.find("div", attrs={"data-name": "Suggestions"}).find_all("a", class_=re.compile("--link--eoxce")):
                print("new {}".format(a.get("href")))
        except Exception as ex:
            print(ex)
            print(f"54 page {time.time() - start_time} second")
            print(20 * "-")



async def gather_data():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": f"{ua.random}"
    }

    #ниже закоментированные строки были сделланы чтоб узннать последнюю страницу но тк их всего 10 оно не надо
    # url = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=1&room1=1&room2=1" 
    async with aiohttp.ClientSession() as session:
        # response = await session.get(url=url, headers=headers, proxy=f"http://g8BapX:NHJ5bk@{choice(proxy)}")
        # soup = BeautifulSoup(await response.text(), "lxml")
        # page_count = int(soup.find("div", attrs={"data-name": "Pagination"}).find_all("li")[-2].text)

        page_count = 10
        tasks = []

        for page in range(1, page_count + 1):#цикл на добовление задач для сбора ссылок с 10 страниц
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        for i in range(1, 1000):#цикл на сбор доп инфы после основных страниц
            task = asyncio.create_task(extra_page(session))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main(): 
    asyncio.run(gather_data()) #запускаем асинхронный метод
    print(f"54 page {time.time() - start_time} second") #вывод после выполнения


if __name__ == "__main__":
    main()

#подсказки для себя самого
# https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=54&region=1&room1=1&room2=1&room3=1
# https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=54&region=1&room1=1&room2=1&room3=1#
# response.json()
# реализовать постоянную подгрузку с проверкой на схожость
# create table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE users(
    #             id serial PRIMARY KEY,
    #             first_name varchar(50) NOT NULL,
    #             nick_name varchar(50) NOT NULL);"""
    #     )
    #     print("Create done!")

    # add in to db something
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO users (first_name,nick_name) VALUES
    #         ('oLeZkA','baba');"""
    #     )
    #     print("db inserted")

    # search in table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """SELECT nick_name FROM users WHERE first_name = 'oLeZkA';"""
    #     )
    #
    #     print(cursor.fetchone())

    # -table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """DROP TABLE users;"""
    #     )
    #
    #     print("gg -table")

    #