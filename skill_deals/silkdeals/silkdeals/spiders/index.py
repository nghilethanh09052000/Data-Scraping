import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector

class IndexSpider(scrapy.Spider):
    name = 'index'
  

    def start_requests(self):
        yield SeleniumRequest(
            url='https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']

        search_input = driver.find_element(By.ID,'search_form_input_homepage')
        search_input.send_keys('Hello World')
        search_input.send_keys(Keys.ENTER)
        
        html = driver.page_source
        response_obj = Selector(text=html)

        links = response_obj.xpath('//div[@class="nrn-react-div"]/article/div[1]/div/a')
        for link in links:
            yield {
                'URL': link.xpath(".//@href").get()
        }
      