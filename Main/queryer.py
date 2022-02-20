# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import sys

import sqlite3
import jieba

def get_most_k_value(k, li):
    counter = dict()
    for item in li:
        if item not in counter:
            counter[item] = 1
        else:
            counter[item] += 1
    ret = sorted(counter.items(), key=lambda d: d[1], reverse=True)
    return [x[0] for x in ret][:k]


class SQL_queryer(object):
    def __init__(self, database_filename):
        self.conn = sqlite3.connect(database_filename)

    def queryer_help(self, word):
        ret_seq = self.conn.execute("SELECT * FROM WORDS WHERE ID = '" + word + "'")
        final_list = []
        for item in ret_seq:
            tmp_str = item[1]
            str_list = tmp_str.split(',')
            int_list = [int(x) for x in str_list]
            for x in int_list:
                final_list.append(x)
        return final_list

    def query(self, strings):

        words = jieba.cut_for_search(strings)
        raw_list = []
        for word in words:
            raw_list.extend(self.queryer_help(word))
        return get_most_k_value(100, raw_list)

