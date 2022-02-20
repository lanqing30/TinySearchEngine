# -*- coding: utf-8 -*-
import sys
import jieba


import web
from queryer import *
from object_constructor import *

import time


urls = ('/Binoocle', 'Index')
app = web.application(urls, globals())
render = web.template.render('templates')


def log(className):
    timer = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    visiter_ip = web.ctx['ip']
    f = open('log.txt', 'a+')
    string = (className + ' ' + timer + ' ' + visiter_ip + '\n')
    f.write(string.encode('utf-8'))
    f.close()



class Index:
    def GET(self):
        log('IndexGet ')
        return render.index()

    def POST(self):
        # unicode
        contents = web.input()['title']

        sq = SQL_queryer('my_engine_data_base.db')
        log('IndexPost ' + contents)
        index_list = sq.query(contents)

        shows = []
        for index in index_list:
            try:
                shows.append(ObjectConstructor(index, contents))
            except:
                print 'failed @ ' + str(index)
        return render.main(shows)


if __name__ == '__main__':
    print('Ready...')
    app.run()

