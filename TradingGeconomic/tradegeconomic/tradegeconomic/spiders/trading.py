import scrapy


class TradingSpider(scrapy.Spider):
    name = 'trading'
    allowed_domains = ['tradingeconomics.com']
    start_urls = ['http://tradingeconomics.com/country-list/government-debt-to-gdp']

    def parse(self, response):
        countries = response.xpath('//table//tr')
        for country in countries:
            country_name = country.xpath('.//td[1]/a').xpath("normalize-space()").get()
            country_last = country.xpath('.//td[2]/text()').get()
            country_prev = country.xpath('.//td[3]/text()').get()
            country_pref = country.xpath('.//td[4]/span/text()').get()
            yield {
                'Country': country_name,
                'Last': country_last,
                'Previous': country_prev,
                'Reference': country_pref,
            }
