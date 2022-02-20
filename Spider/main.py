

from spider import *
from constructor import *

import time
import os

import logging
logging.basicConfig(level=logging.INFO)


start = time.clock()
logging.info('Spider_Start')
spider = Spider('http://news.dlut.edu.cn/info/1003/51271.htm')
spider.start()
end = time.clock()
logging.info('Over Spider cost ' + str(end-start) + ' second')

start = time.clock()
logging.info('construct and write start')
ctr = Contructor(spider.get_cache())
ctr.construct_and_write()
end = time.clock()
logging.info('Over construct and write cost ' + str(end-start) + ' second')

dev = spider.get_cache()
del dev


start = time.clock()
logging.info('write to sqlite start')
ctr.write_to_sqlite()
end = time.clock()
logging.info('Over write to sqlite cost ' + str(end-start) + ' second')

dev = ctr.get_cache()
del dev

