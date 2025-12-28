#!/usr/bin/env python3
import sys

import requests


def main():
    url = "http://icanhazip.com/"
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    response = requests.get(url, proxies=proxies)
    print('tor ip: {}'.format(response.text.strip()))


if __name__ == "__main__":
    sys.exit(main())
