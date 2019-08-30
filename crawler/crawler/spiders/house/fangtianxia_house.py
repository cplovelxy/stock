import scrapy


class ftxHouse(scrapy.Spider):
    name = 'ftx_house'

    def start_requests(self):
        urls = ['https://sz.newhouse.fang.com/house/s/', 'https://sz.esf.fang.com/?ctm=1.sz.xf_search.head.140']
        for url in urls:
            yield scrapy.Request(url =url,  callback=self.parse)

    def parse(self, response):
        all_house_dl = response.css('div.shop_list_4 dl')
        house_items = []

        for house_dl in all_house_dl:
            house_dict = {}
            house_image = house_dl.css('dt a img::attr(src)').get()
            house_dict['house_image'] = house_image
            # 房屋基本信息 2室2厅 |78㎡ |高层（共28层） |南向 |2001年建
            house_base = house_dl.css('dd p.tel_shop::text').getall()
            house_dict['house_base'] = house_base
            house_address = house_dl.css('dd p.add_shop a::attr(title)').get() + house_dl.css('dd p.add_shop span::text').get()
            house_dict['house_address'] = house_address
            # 满五优质教育业主急售黄金楼层距3号线华新站约176米
            house_other = house_dl.css('dd p.clearfix span::text').getall()
            house_dict['house_other'] = house_other
            house_price = house_dl.css('dd.price_right span.red b::text').get() + house_dl.css('dd.price_right span::text')[0].get()
            house_dict['house_price'] = house_price
            house_size = house_dl.css('dd.price_right span::text')[1].get()
            house_dict['house_size'] = house_size
            house_items.append(house_dict)
        print(house_items)
