#!/usr/bin/env python3
import unittest

import web_scraping as ws


class WebScrapingTest(unittest.TestCase):
    FILE_URL = "main_news.html"

    def setUp(self):
        print('setUp called')
        pass

    def tearDown(self):
        print('tearDown called')
        pass

    def test_(self):
        ws.parse_and_process(open(self.FILE_URL))

if __name__ == '__main__':
    unittest.main()
