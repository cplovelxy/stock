import scrapy

class shoeSiders(scrapy.Spider):
    name = "duAppShoeSiders"
    url = ["http://wdywt.cn/goodslist/1/sort/new"]

    def parse(self, response):
        print()
