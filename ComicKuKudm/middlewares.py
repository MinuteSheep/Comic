# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent


class RandomUserAgentMiddlware(object):
    # 随机更换user-agent

    def __init__(self, crawler):
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        print(self.ua)
        request.headers.setdefault("User-Agent", self.ua.random)
