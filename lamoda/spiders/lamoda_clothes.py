import socket
import scrapy
import re

from scrapy.loader.processors import MapCompose, Join
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.http import Request
from re import findall

from properties.items import PropertiesItem


class LamodaSpider(scrapy.Spider):
    name = "lamoda_clothes"
    allowed_domains = ["www.lamoda.ua"]

    start_urls = (
        'https://www.lamoda.ua/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=2&page=1',
    )
    def parse(self, response):
        number_of_elements = response.xpath('(//span[@class="cat-nav-cnt"])[2]/text()').get()
        number_of_elements = int(str(number_of_elements))//120
        current_page_url = findall(r'(.*)&page=', response.url)[0]
        for page_number in range(1,number_of_elements):
            next_page_url = f"{current_page_url}&page={page_number}"
            yield Request(response.urljoin(next_page_url))
        item_selector = response.xpath('//a[@class="products-list-item__link link"]/@href')
        for url in item_selector.extract():
            yield Request(response.urljoin(url),callback=self.parse_items)

    def parse_items(self, response):
        first_price = response.xpath('//*[contains(@class,"product-prices__price_current")]/text()').extract()
        first_price = re.sub(r'[^0-9]',"", str(first_price).strip().replace(' ', ''))
        price_current = response.xpath('//*[contains(@class,"product-prices__price_current")]/@content').extract()
        price_current = re.sub(r'[^0-9]',"", str(price_current).strip().replace(' ', ''))
        if price_current == first_price:
            first_price='missing'
        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath('category', '//span[@class="product-title__model-name"]/text()'), MapCompose(str.strip, str.title)
        l.add_xpath('title', '//*[@class="product-title__brand-name"]/@title'), MapCompose(str.strip, str.title)   
        l.add_xpath('article', '//div[@class="ii-product__attribute"]/span[@class="ii-product__attribute-value"]/text()',MapCompose(str.strip),re='[A-Za-z0-9]{12}')  
        l.add_xpath('price_current', '//*[contains(@class,"product-prices__price_current")]/@content',MapCompose(lambda i: i.replace(' ', ''),str.strip),re='[\s,.0-9]+')
        l.add_value('first_price', first_price, MapCompose(lambda i: i.replace(' ', ''),str.strip),re='[\s,.0-9]+')
        l.add_xpath('image_url', '//div[@class="ii-product"]/@data-image', MapCompose(lambda i: response.urljoin(i)))
        yield l.load_item()
