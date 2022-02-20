
import queue
import threading
from urllib import request
from bs4 import BeautifulSoup
from url import URL

import logging
logging.basicConfig(level=logging.INFO)


def urlfilter(current_url, target_url):
    """only for dult news webpage"""
    if not target_url:
        return None
    if target_url.startswith('http://'):
        if target_url.startswith('http://news.dlut.edu.cn'): return target_url
        else: return None

    current_path = current_url.split('/')
    current_path = current_path[:-1] if current_path[-1] == '' else current_path
    current_path = current_path[:-1]

    target_path = target_url.split('/')
    target_path = target_path[:-1] if target_path[-1] == '' else target_path

    for path_item in target_path:
        if path_item == '..':
            current_path.pop()
        else:
            current_path.append(path_item)
    return 'http://' + '/'.join(current_path)


class Spider(object):
    def __init__(self, root_url):
        self.root_url = root_url
        self.url_queue = queue.Queue()
        self.seen = set()
        self.global_cache = []
        self.global_url_counter = 0

    def one_thread(self, start_url):
        self.url_queue.put(start_url)
        self.seen.add(start_url)
        while not self.url_queue.empty():
            current_url = self.url_queue.get()  # fetch the first url
            extract_urls = []
            try:
                extract_urls = self.save_and_extract(current_url)
            except TimeoutError:
                break
            for next_link in extract_urls:
                if next_link in self.seen:
                    continue
                self.seen.add(next_link)
                self.url_queue.put(next_link)




    def save_and_extract(self, url):
        req = request.Request(url)
        req.add_header('User-Agent', 'Mozilla/6.0')
        try:
            req = request.urlopen(req).read().decode('utf-8')
        except:
            print('failed ', url)
            return []

        soup = BeautifulSoup(req, 'lxml')

        # TODO: bs libary doesn't work here.
        def get_title(html_str):
            i = html_str.find('<title>')
            j = html_str.find('</title>')
            if i == -1 or j == -1:
                i = html_str.find('<TITLE>')
                j = html_str.find('</TITLE>')
            tmpRes = html_str[i + 7:j]
            if tmpRes.endswith('-大连理工新闻网'):
                return tmpRes[:-8]
            else:
                return tmpRes

        paragraphs_source = soup.find('div', id='vsb_content_500')
        post_time_source = soup.find('span', class_="post-time")

        page_main_text = paragraphs_source.get_text() if paragraphs_source else ''
        post_time = post_time_source.get_text() if post_time_source else '1970-01-01 00:00'
        page_title = get_title(req)

        link_to = []
        links = soup.find_all('a')
        for link in links:
            tmp = urlfilter(url[7:], link.get('href'))
            if tmp:
                link_to.append(tmp)

        self.global_cache.append(URL(url, self.global_url_counter, page_title, page_main_text, link_to, post_time))
        self.global_url_counter += 1

        # check the number
        # print(self.global_url_counter)
        if self.global_url_counter % 100 == 0:
            logging.info('Spider_has_clawed ' + str(self.global_url_counter) + ' items...')

        # uncomment this line when this programme is running on the server.
        if self.global_url_counter >= 30:
            raise TimeoutError()

        return link_to

    def start(self):
        self.one_thread(self.root_url)

    def get_cache(self):
        return self.global_cache



