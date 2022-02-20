# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import sys
import json

class ObjectConstructor(object):

    def __init__(self, index, queryword):
        with open('./info/' + str(index) + '.txt', 'r') as f:
            self.data = json.load(f)
            self.key_words = list(queryword)

    def get_title(self):
        title = ''
        for char in self.data['title']:
            if char in self.key_words:
                char = '<strong>' + char + '</strong>'
            title += char
        return title

    def get_text(self):
        string = self.data['text']
        cur = string.find(self.key_words[0])
        i = max(0, cur - 40)
        j = cur + 90
        origin = string[i:j]
        returnString = ''
        for char in origin:
            if char in self.key_words:
                char = '<strong>' + char + '</strong>'
            returnString += char
        return returnString


    def get_url_ori(self):
        return self.data['url']

