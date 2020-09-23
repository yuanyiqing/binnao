# -*- coding: utf-8 -*

import requests
from requests.adapters import HTTPAdapter
import time
import json
from lxml import etree

base = 'http://www.binnao.com/forum-87-%d.html'

ignore = [
    'http://www.binnao.com/thread-94113-1-1.html',
    'http://www.binnao.com/thread-81838-1-1.html',
    'http://www.binnao.com/thread-102144-1-1.html',
    'http://www.binnao.com/thread-122801-1-1.html',
    'http://www.binnao.com/thread-99738-1-1.html',
    'http://www.binnao.com/thread-106260-1-1.html',
    'http://www.binnao.com/thread-366426-1-1.html',
    'http://www.binnao.com/thread-366455-1-1.html',
    'http://www.binnao.com/thread-388932-1-1.html',
    'http://www.binnao.com/thread-366423-1-1.html'
]

books = dict()

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=5))
s.mount('https://', HTTPAdapter(max_retries=5))

page_num = 0
try:
    result = s.get(base % 1, timeout=(3, 3))
    html = etree.HTML(result.content)
    number = html.xpath('//a[@class="last"]/text()')[0].split(' ')[1]
    page_num = int(number)
except Exception as e:
    print('fetch page number failed')

if page_num > 0:
    for page in range(1, page_num + 1):
        try:
            result = s.get(base % page, timeout=(3, 3))
        except Exception as e:
            print('fetch page %d failed' % page)
            continue

        html = etree.HTML(result.content)
        paths = html.xpath('//a[@class="s xst"]/@href')
        names = html.xpath('//a[@class="s xst"]/text()')

        for j in range(0, len(paths)):
            if page != 1 or paths[j] not in ignore:
                books[paths[j]] = names[j]

        print('page %d done.' % page)
        time.sleep(0.1)

    with open('book_list.json', 'w') as book_list:
        json.dump(books, book_list)
else:
    print('No page number')
