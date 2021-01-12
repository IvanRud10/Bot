from scrapy.item import Item, Field


class PropertiesItem(Item):
    title = Field()
    category = Field()
    article = Field()
    first_price = Field()
    price_current = Field()
    image_url = Field()
    number_of_elements = Field()

