import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector


class ComputerSpider(scrapy.Spider):
    name = 'computer'
    allowed_domains = ['slickdeals.net']
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals']/li")
        for product in products:
            yield {
                'name': product.xpath(".//a[@class='itemTitle']/text()").get(),
                'link': product.xpath(".//a[@class='itemTitle']/@href").get(),
                'store_name': self.remove_characters(product.xpath("normalize-space(.//span[@class='itemStore']/text())").get()),
                'price': product.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()
            }

        # next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        # if next_page:
        #     absolute_url = f"https://slickdeals.net{next_page}"
        #     yield SeleniumRequest(
        #         url=absolute_url,
        #         wait_time=3,
        #         callback=self.parse
        #     )
