from bs4 import BeautifulSoup

import requests

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options

from webdriver_manager.core.utils import ChromeType
# 크롬 드라이버 자동 업데이트

from webdriver_manager.chrome import ChromeDriverManager

import time

import json

url = 'https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=genre&genreCode=207&orderTypeCode=sale&is&isFinished=false'
req_header_dict = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

chrome_service = Service(ChromeDriverManager(
    chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get(url)

time.sleep(1)

for i in range(10):
    driver.execute_script("window.scrollBy(0, " + str((i + 1) * 70) + ")")
    time.sleep(1)


html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

items = soup.select(
    "#content > div > ul > li > div > h3 > a")

book_list = []
book_detail_list = []

for e, item in enumerate(items, 1):

    book_dict = {}
    # book_thumb = soup.select_one("#content > div > ul > li > a > img")["src"]
    book_dict['index'] = e
    book_dict['title'] = item.text
    book_url_pre = item.get('href')
    book_id = book_url_pre[31:38].replace("?", "")
    book_dict['id'] = book_id
    book_url = f"https://series.naver.com/novel/detail.series?productNo={book_id}"
    # book_dict['thumbs'] = book_thumb
    book_dict['url'] = book_url

    book_list.append(book_dict)

for idx, book in enumerate(book_list, 1):
    book_detail_dict = {}
    book_detail_url = book['url']

    res2 = requests.get(book_detail_url, headers=req_header_dict)
    # print(res.status_code)
    soup2 = BeautifulSoup(res2.text, 'html.parser')

    book_detail_dict['index'] = book['index']
    book_detail_dict['title'] = book['title']
    book_detail_dict['id'] = book['id']
    book_detail_dict['url'] = book['url']

    book_thumbs = soup2.select_one(
        "#container > div.aside.NE\=a\:nvi > a > img")['src']

    book_detail_dict['thumb'] = book_thumbs
    book_detail_list.append(book_detail_dict)

print(book_detail_list)

with open('series_rf_top25.json', 'w', encoding='utf-8') as file:
    json.dump(book_detail_list, file, ensure_ascii=False)

driver.quit()
