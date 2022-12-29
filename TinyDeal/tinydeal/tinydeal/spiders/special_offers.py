import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html/']

    def parse(self, response):
        products = response.xpath('//ul[@class="productlisting-ul"]/div[@class="p_box_wrapper"]/li')
        for product in products:
            yield {
                "Title": product.xpath('.//a[@class="p_box_title"]/text()').get(),
                "Url": response.urljoin(product.xpath('.//a[@class="p_box_title"]/@href').get()),
                "Discounted Price": product.xpath('.//div[@class="p_box_price"]/span[1]/text()').get(),
                "Original Price": product.xpath('.//div[@class="p_box_price"]/span[2]/text()').get(),
            }
        next_page = response.xpath('//a[@class="nextPage"]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

