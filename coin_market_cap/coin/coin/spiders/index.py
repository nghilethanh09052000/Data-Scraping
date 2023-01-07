# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware
class IndexSpider(CrawlSpider):
    
    name = 'index'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/']
    
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//tbody/tr/td/a[@class="cmc-link"]'), 
            callback='parse_item', 
            follow = True
        ),
    )


    def parse_item(self, response):
        name = response.xpath('//span[@class="sc-1d5226ca-1 fLa-dNu  "]/text()').get()
        price = response.xpath('//div[@class="priceValue "]/span/text()').get()
        rank = response.xpath('//div[@class="namePill namePillPrimary"]/text()').get()
        yield {
            'Name': name,
            'Price': price,
            'Rank': rank
        }
