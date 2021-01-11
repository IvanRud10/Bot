import datetime
import socket
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from re import findall

from properties.items import PropertiesItem


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["www.lamoda.ua"]

    # Start on the first index page
    start_urls = (
        'https://www.lamoda.ua/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=2&page=1',
    )
    def parse(self, response):
        """
        current_page_number = int(findall(r'&page=(.*)', response.url)[0])
        current_page_url = findall(r'(.*)&page=', response.url)[0]
        yield Request(response.urljoin(current_page_url),callback=self.parse1)
        next_page_number = current_page_number + 1
        next_page_url = f"{current_page_url}&page={next_page_number}"
        yield Request(response.urljoin(next_page_url),callback=self.parse1)
        """
        for x in range(168):
            current_page_url = findall(r'(.*)&page=', response.url)[0]
            next_page_url = f"{current_page_url}&page={x}"
            yield Request(response.urljoin(next_page_url),callback=self.parse1)
    def parse1(self, response):
        item_selector = response.xpath('//a[@class="products-list-item__link link"]/@href')
        for url in item_selector.extract():
            yield Request(response.urljoin(url),callback=self.parse_items)
        #item_selector1 = str(item_selector)
        #item_selector2 = f"https://www.lamoda.ua{item_selector1}"
        #yield Request(response.urljoin(item_selector2),callback=self.parse_items)

    def parse_items(self, response):
        #price = response.xpath('//span[@class="_1xktn17sNuFwy45DZmZ5Oe product-prices__price_current"]/span[@style="white-space: nowrap;"]/text()').get()
        price1 = response.xpath('//span[contains(@class,"CQSDz7BBEVO3V9K8bKMYg")]/span/text()',re='[\s,.0-9]+').extract()
        if not price1:
            price1='missing'
        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath('category', '//span[@class="product-title__model-name"]/text()'), MapCompose(str.strip, str.title)
        l.add_xpath('title', '//*[@class="product-title__brand-name"]/@title'), MapCompose(str.strip, str.title)   
        l.add_xpath('article', '//div[@class="ii-product__attribute"]/span[@class="ii-product__attribute-value"]/text()',MapCompose(str.strip),re='[A-Za-z0-9]{12}')  
        #l.add_xpath('price1', '//*[contains(@class,"CQSDz7BBEVO3V9K8bKMYg")]/text()',MapCompose(lambda i: i.replace(',', ''),str.strip),re='[\s,.0-9]+')
        l.add_xpath('price_current', '//*[contains(@class,"product-prices__price_current")]/text()',MapCompose(lambda i: i.replace(',', ''),str.strip),re='[\s,.0-9]+')
        #l.add_xpath('price_current', '//*[contains(text(),"₴")]/text()',MapCompose(lambda i: i.replace(',', ''),str.strip),re='[\s,.0-9]+')
        #l.add_xpath('price', '//*[@class="_1xktn17sNuFwy45DZmZ5Oe product-prices__price_current"]/span[@style="white-space: nowrap;"]/text()',MapCompose(lambda i: i.replace(',', ''), float),re='[,.0-9]+')
        l.add_xpath('image_url', '//img[@class="swiper-lazy x-gallery__image x-image__zoom-in swiper-lazy-loaded"][1]/@src')
        l.add_value('price1',price1)
        yield l.load_item()

