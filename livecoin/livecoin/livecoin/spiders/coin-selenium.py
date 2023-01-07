import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
from selenium.webdriver.common.by import By

class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin-selenium'
    allowed_domains = ['web.archive.org']
    start_urls = [
        "https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/"
    ]

    def __init__(self):

        chrome_option = Options()
        chrome_option.add_argument("--headless")

        chrome_path = which("chromedriver")

        driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_option)
        driver.get("https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/")

        rur_tab = driver.find_elements(By.CLASS_NAME,value="filterPanelItem___2z5Gb ")
        rur_tab[4].click()
        self.html = driver.page_source
        driver.close()



  
    def parse(self, response):
        res = Selector(text=self.html)
        currencies = res.xpath('//div[@class="tableRow___3EtiS "]')
        for currency in currencies:
            yield {
                'Coin' : currency.xpath('.//div[1]/div/text()').get(),
                'Volume (24h)': currency.xpath('.//div[2]/span/text()').get(),
                'Last Price': currency.xpath('.//div[3]/span/text()').get(),
                'Change (24h)':  currency.xpath('.//div[4]/span/text()').get()
            }
