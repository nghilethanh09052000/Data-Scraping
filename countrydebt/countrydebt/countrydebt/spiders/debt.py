import scrapy
from scrapy_splash import SplashRequest

class DebtSpider(scrapy.Spider):
    name = 'debt'
    allowed_domains = ['worldpopulationreview.com']
    
    def start_requests(self):
        yield SplashRequest(
            url = 'https://worldpopulationreview.com/country-rankings/countries-by-national-debt'
        )

    def parse(self, response):
        pass
