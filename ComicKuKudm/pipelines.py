# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class ImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['image']['image_url']
        yield scrapy.Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image']['download_path'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        chapter_name = request.meta['item']['image']['chapter_name']
        request.meta['item']['image']['image_name'] = request.meta['item'][
            'image']['web_page'].split('/')[-1].split('.')[0].strip() + '.jpg'
        path = chapter_name + '/' + request.meta['item']['image']['image_name']
        return path
