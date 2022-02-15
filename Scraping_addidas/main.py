import json
import requests
import csv
import re
from bs4 import BeautifulSoup
from datetime import datetime

def get_some_shoes_on_sale():
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36"
    }

    url = "https://www.adidas.cz/obuv-originals?start=0&v_size_cs_cz=45"
    req = requests.get(url, headers=headers)
    src = req.text
    with open("index.html", "w", encoding="UTF-8-sig") as file:
        file.write(src)

    # with open("index.html", "r+", encoding="UTF-8-sig") as file:
    #     src = file.read()
    soup = BeautifulSoup(src, "lxml")
    page_all_number = int(soup.find(class_=re.compile("pagination")).find_all("span", class_="gl-label gl-label--l")[-1].text.split("/")[-1])

    data = []
    for i in range(0, page_all_number*48+1, 48):
        url = f"https://www.adidas.cz/obuv-originals?start={i}&v_size_cs_cz=45"
        req = requests.get(url, headers=headers)
        src = req.text

        with open(f"data/index{i}.html", "w", encoding="UTF-8-sig") as file:
            file.write(src)

        cur_date = datetime.now().strftime("%d_%m_%Y")
        with open(f"data_{cur_date}.csv", "w", encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    "product_article",
                    "product_url",
                    "product_price"
                )
            )
        soup = BeautifulSoup(src, "lxml")
        shoes_link = soup.find("div", class_=re.compile("plp-grid")).find_all("a")
        for element in shoes_link:
            article_text = element.get("href")
            shoes = article_text.split("/")[1]
            url = "https://www.adidas.cz" + article_text
            req = requests.get(url, headers=headers)
            src = req.text
            with open(f"shoes_page/{i}_{shoes}.html", "w", encoding="UTF-8-sig") as file:
                file.write(src)
            # with open(f"shoes_page/{i}_{shoes}.html", "r+", encoding="UTF-8-sig") as file:
            #     src = file.read()
            soup = BeautifulSoup(src, "lxml")
            try:
                cost_shoes = soup.find("div", class_=re.compile("gl-price-item")).text
            except Exception as ex_:
                print(ex_)
                print(shoes)
                print(url)
            cost_shoes = cost_shoes.replace(" ", " ")
            data.append(
                {
                    "product_article": shoes,
                    "product_url": url,
                    "product_price": cost_shoes
                }
            )
            with open(f"data_{cur_date}.csv", "a", encoding="UTF-8") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        shoes,
                        url,
                        cost_shoes
                    )
                )
    with open(f"data_{cur_date}.json", "a", encoding="UTF-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    get_some_shoes_on_sale()


if __name__ == "__main__":
    main()
