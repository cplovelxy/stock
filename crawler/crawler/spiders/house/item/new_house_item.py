import scrapy


class NewHouse(scrapy.Item):
    house_image = scrapy.Field()
    house_name = scrapy.Field()
    house_price = scrapy.Field()
    house_address = scrapy.Field()
