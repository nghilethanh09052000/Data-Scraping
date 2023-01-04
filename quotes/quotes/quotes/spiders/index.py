import scrapy
from scrapy_splash import SplashRequest



class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['quotes.toscrape.com']
    
    script = '''
       function main(splash, args)
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return html = splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url = f'http://quotes.toscrape.com/js/',
            callback = self.parse,
            args = {
                'wait': 1,
                'lua_source': self.script
            }
        )
    
    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            yield {
                'Quote': quote.xpath('.//span[1]/text()').get(),
                'Author': quote.xpath('.//span[2]/small/text()').get(),
            }
        next_page = response.xpath('//nav/ul/li[@class="next"]/a/@href').get()
        if next_page: 
            print(next_page)
            yield SplashRequest(
                url = f"http://quotes.toscrape.com{next_page}",
                callback = self.parse,
                args = {
                    'wait': 1,
                    'lua_source': self.script
                }
            )
        
