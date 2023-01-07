import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['web.archive.org']
   
    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(5))
            return {
                html = splash:html(),
            }
        end

    '''
    def start_requests(self):
        yield SplashRequest(
            url="https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/", 
            callback=self.parse, 
            endpoint="execute", 
            args={
                'lua_source': self.script
            })

   
  
    def parse(self, response):
        print(response)
        # currencies = response.xpath('//div[@class="tableRow___3EtiS "]')
        # for currency in currencies:
        #     yield {
        #         'Coin' : currency.xpath('.//div[1]/div/text()').get(),
        #         'Volume (24h)': currency.xpath('.//div[2]/span/text()').get(),
        #         'Last Price': currency.xpath('.//div[3]/span/text()').get(),
        #         'Change (24h)':  currency.xpath('.//div[4]/span/text()').get()
        #     }
