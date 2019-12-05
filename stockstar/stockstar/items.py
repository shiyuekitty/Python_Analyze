# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
class StockstarItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class StockstarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    abbr = scrapy.Field()
    last_trade = scrapy.Field()
    chg_ratio = scrapy.Field()
    chg_amt = scrapy.Field()
    chg_ratio_5min = scrapy.Field()
    volumn = scrapy.Field()
    turn_over = scrapy.Field()
