from scrapy.item import Item, Field


class PropertiesItem(Item):
    # Primary fields
    title = Field()
    price = Field()
    description = Field()
    address = Field()
    image_urls = Field()

    # Calculated fields
    images = Field()
    location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()

    category = Field()
    article = Field()
    first_price = Field()
    price_current = Field()
    image_url = Field()
    number_of_elements = Field()

