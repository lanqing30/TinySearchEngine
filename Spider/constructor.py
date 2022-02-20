
import json
import jieba
from sqliter import SQL

import logging
logging.basicConfig(level=logging.INFO)


def get_most_k_value(k, li):
    counter = dict()
    for item in li:
        if item not in counter:
            counter[item] = 1
        else:
            counter[item] += 1
    ret = sorted(counter.items(), key=lambda d: d[1], reverse=True)
    return [x[0] for x in ret][:k]


class Contructor(object):
    def __init__(self, urls):
        self.url_to_id = dict()
        self.urls = urls # caches
        self.hashing = dict() 
        self.sql = SQL('../Main/my_engine_data_base.db')

    def construct_and_write(self):
        for urlobj in self.urls:
            self.url_to_id[urlobj.url] = urlobj.id
        # may be we should dump the url-id dict to the file as a json format.

        counter = 0
        for urlobj in self.urls:
            counter += 1
            if counter % 100 == 0:
                logging.info('ctr has written file... ' + str(counter) + ' items...')
            for link in urlobj.links:
                if link in self.url_to_id:
                    urlobj.links_id.append(self.url_to_id[link])

        for urlobj in self.urls:

            data = {
                'url': urlobj.url,
                'title': urlobj.title,
                'time': urlobj.time,
                'rank': urlobj.rank,
                'text': urlobj.text
            }

            words = jieba.cut_for_search(urlobj.text)
            for word in words:
                if word not in self.hashing: self.hashing[word] = [urlobj.id]
                else: self.hashing[word].append(urlobj.id)

            with open('../Main/info/' + str(urlobj.id) + '.txt', 'w+', encoding='utf-8') as f:
                json.dump(data, f)


    # preprocess
    def write_to_sqlite(self):
        for word, indexlist in self.hashing.items():
            self.hashing[word] = get_most_k_value(100, indexlist)
            self.sql.Insert(word, self.hashing[word])
        self.sql.Close()

    def get_cache(self):
        return self.hashing


