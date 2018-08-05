#!/usr/bin/env python3
import re
import sys
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

WIKI_URL = "https://ko.wikipedia.org/wiki/%ED%8F%AC%ED%84%B8:%EC%9A%94%EC%A6%98_%ED%99%94%EC%A0%9C"

def request(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "close"
    }
    return session.get(url, headers=headers).content

def urllib_request(url):
    return urlopen(url)

def parse_and_process(html):
    bsObj = BeautifulSoup(html, "html.parser")
    main_news = bsObj.find("table", {"class": "vevent"})
    tr_all = main_news.find("table").find_all("tr")

    # title
    print(tr_all[0].get_text().strip())

    # ui list
    news_all = tr_all[1].find_all("li")

    for each_tr in news_all:
        text = each_tr.get_text().strip().replace("\n", " ")
        striped_text = re.sub('\s\s+', " ", text)
        print(striped_text)

def main():
    # html = urllib_request(WIKI_URL)

    html = request(WIKI_URL)
    parse_and_process(html)

if __name__ == "__main__":
    sys.exit(main())
