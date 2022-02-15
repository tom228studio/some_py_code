from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool
from fake_useragent import UserAgent
from random import choice
# from seleniumwire import webdriver
import random
import time
import pickle

proxy = open("D:\\some_py_code\\git1\\scraper_cian-main\\proxy").read().split('\n')

ua = UserAgent()
options = webdriver.ChromeOptions()

# prox = Proxy()
# prox.proxy_type = ProxyType.MANUAL
# prox.http_proxy = "ip_addr:port"
# prox.socks_proxy = "ip_addr:port"
# prox.ssl_proxy = "ip_addr:port"
#
# capabilities = webdriver.DesiredCapabilities.CHROME
# prox.add_to_capabilities(capabilities)
#
# driver = webdriver.Chrome(desired_capabilities=capabilities)
def get_data(url):
    try:
        for i in range(100):
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument(f"user-agent={ua.random}")
            options.add_argument(f"--proxy-server={choice(proxy)}")
            options.add_argument("accepts")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        # del driver.request.headers['accept']
        # driver.request.headers['accept'] = 'text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9'
        driver.get(url=url)
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
        except Exception as ex:
            pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        time.sleep(random.randrange(10, 16))

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

if __name__ == '__main__':
    url = "https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=54&region=1&room1=1&room2=1#"
    # url = "https://www.2ip.ru/"
    get_data(url)

