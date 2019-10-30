# -*- coding: utf-8 -*-
from scrapy import Spider, Request, shell
import re
from ComicKuKudm.items import ComicItem


class ComicSpider(Spider):
    name = 'comic'
    allowed_domains = ['kukudm.com']
    start_urls = ['http://comic.ikkdm.com/comiclist/2126/']
    img_server = 'http://n9.1whour.com/'
    chapter_server = 'http://comic.kukudm.com'
    img_patten = re.compile('.*?\+"(.*?)\'></a>')
    mp_patten = re.compile('.*?共(\d+)页')

    def start_requests(self, ):
        yield Request(url=self.start_urls[0], callback=self.parse_index)

    def parse_index(self, response):
        chapter_urls = response.css('dd a:first-child::attr(href)').extract()
        chapter_names = response.css('dd a:first-child::text').extract()
        for chapter_name, chapter_url in zip(chapter_names, chapter_urls):
            item = ComicItem()
            item['chapter_url'] = self.chapter_server + chapter_url
            item['chapter_name'] = chapter_name
            yield Request(url=item['chapter_url'],
                          meta={'item': item},
                          callback=self.parse_page)

    def parse_page(self, response):
        item = response.meta['item']
        max_page = int(
            re.findall(self.mp_patten,
                       response.css('td::text').extract_first())[0])
        per_url = item['chapter_url'].strip(
        )[:-len(item['chapter_url'].strip().split('/')[-1])]
        for i in range(1, max_page + 1):
            new_url = per_url + str(i) + '.htm'
            yield Request(url=new_url,
                          callback=self.parse_img,
                          meta={
                              'item': item,
                          })

    def parse_img(self, response):
        item = response.meta['item']
        item['name_url'] = response.url
        item['image_urls'] = [
            self.img_server +
            re.findall(self.img_patten,
                       response.css('script::text').extract_first())[0]
        ]
        return item
