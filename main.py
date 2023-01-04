from bs4 import BeautifulSoup

import requests

import json

url = 'https://series.naver.com/novel/categoryProductList.series?categoryTypeCode=genre&genreCode=207&orderTypeCode=sale&is&isFinished=false'
req_header_dict = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


res = requests.get(url, headers=req_header_dict)


html = res.text

soup = BeautifulSoup(html, "html.parser")

rank = 0
books = soup.select(
    "#content > div > ul > li > div > h3 > a")
book_thumbs = soup.select(
    "#content > div > ul > li > a > img")
book_stars = soup.select(
    "#content > div > ul > li > div > p.info > em.score_num")
book_authors = soup.select(
    "#content > div > ul > li > div > p.info > span:nth-child(4)")


book_list = []

for book, book_thumb, book_star, author in zip(books, book_thumbs, book_stars, book_authors):
    book_dict = {}

    rank = rank + 1
    book_url_pre = book.get('href')
    book_id = book_url_pre[31:38].replace("?", "")
    book_url = f"https://series.naver.com/novel/detail.series?productNo={book_id}"
    book_dict['id'] = book_id
    book_dict['index'] = rank
    book_dict['title'] = book.text
    book_dict['url'] = book_url
    book_dict['thumb'] = book_thumb.get('src')
    book_dict['star'] = book_star.text
    book_dict['author'] = author.text
    book_list.append(book_dict)


with open('series_rf_top25.json', 'w', encoding='utf-8') as file:
    json.dump(book_list, file, ensure_ascii=False)
