import scrapy
import json
from scrapy.exceptions import CloseSpider

class BookSpider(scrapy.Spider):

    name = 'book'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12']
    limit_increment = 0

    def parse(self, response):
        res = json.loads(response.body)
        books = res.get('works')

        if not books:
            raise CloseSpider("No more content to show")

        for book in books:
            yield {
                'Title': book.get('title'),
                'Subject': book.get('subject'),
                'Author': book.get('authors')
            }

        self.limit_increment += 12
        yield scrapy.Request(
            url = f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.limit_increment}',
            callback = self.parse
        )
        

