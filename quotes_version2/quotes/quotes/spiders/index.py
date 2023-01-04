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
            
            while not splash:select('div.quote') do
                splash:wait(0.1)
                print('waiting...')
            end

            local num_scrolls = 10
            local scroll_delay = 1.0
            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                        "function(){return document.body.scrollHeight;}"
            )
            
            for _ = 1, num_scrolls do
                scroll_to(0,get_body_height())
                assert(splash:wait(scroll_delay))
            end
            
            return {
                html = splash:html(),
                png = splash:png()
            }
        end
    '''
    def start_requests(self):
        yield SplashRequest(
            url = 'http://quotes.toscrape.com/scroll',
            callback = self.parse,
            endpoint = 'execute',
            args = {
                'wait': 2,
                'lua_source': self.script,
            }
        )
    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            yield {
                'Quote': quote.xpath('.//span[1]/text()').get(),
                'Author': quote.xpath('.//span[2]/small/text()').get(),
            }
