# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ComicItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    chapter_name = Field()    # chapter name, is also dir name
    chapter_url = Field()     # chapter's url
    img_url = Field()         # images' url
    img_path = Field()        # inamges' name
    
