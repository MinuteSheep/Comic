# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import os
from ComicKuKudm import settings


class ComicDownloadPipline(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    def process_item(self, item, spider):
        dir_path = '%s/%s' % (settings.IMAGE_STORE, item['chapter_name'])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for image_url in item['img_url']:
            image_file_name = '#' + \
                image_url.split('/')[-1].split('.')[0] + '.jpg'
            image_file_path = '%s/%s' % (dir_path, image_file_name)
            if os.path.exists(image_file_path):
                continue

            with open(image_file_path, 'wb') as f:
                response = requests.get(image_url, headers=self.headers)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
