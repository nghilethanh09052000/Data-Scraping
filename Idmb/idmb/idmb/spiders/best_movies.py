import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['web.archive.org']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='http://web.archive.org/web/20200715000935/https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent
        })


    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths='//h3[@class="lister-item-header"]/a'), 
                callback='parse_item', 
                follow=True,
                process_request='set_user_agent'
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths='(//a[@class="lister-page-next next-page"])[2]',
                process_request='set_user_agent'
        ),
    ))

    def set_user_agent(self,request):
        request.headers['User-Agent'] = self.user_agent
        return request


    def parse_item(self, response):
        yield {
            'Title': response.xpath('//div[@class="title_wrapper"]/h1/text()').get(),
            'Year': response.xpath('//div[@class="title_wrapper"]/h1/span[@id="titleYear"]/a/text()').get(),
            'Duration': response.xpath('normalize-space(//div[@class="subtext"]/time/text())').get(),
            'Genre': response.xpath('//div[@class="subtext"]/a/text()').get(),
            'Rating': response.xpath('//div[@class="ratingValue"]/strong/span/text()').get(),
            'Movie Url': response.url,
            'User-Agent': response.request.headers['User-Agent']
        }

