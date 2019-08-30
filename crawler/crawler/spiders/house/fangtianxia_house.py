import scrapy


class ftxHouse(scrapy.Spider):
    name = 'ftx_house'
    allowed_domains = ['sz.newhouse.fang.com', 'sz.esf.fang.com']
    new_house_domain = 'https://sz.newhouse.fang.com'
    old_house_domain = 'https://sz.esf.fang.com'
    new_house_url = 'https://sz.newhouse.fang.com/house/s/'
    old_house_url = 'https://sz.esf.fang.com/?ctm=1.sz.xf_search.head.140'
    cookies = {'Integrateactivity': 'notincludemc', '__utma': '147393320.125060648.1567134119.1567156397.1567159658.4',
               '__utmb': '147393320.33.10.1567159658', '__utmc': '147393320', '__utmt_t0': '1', '__utmt_t1': '1',
               '__utmt_t2': '1', '__utmz':
                   '147393320.1567156397.3.3.utmcsr=sz.newhouse.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/house/s/b92/',
               'city': 'sz', 'g_sourcepage': 'ehlist', 'global_cookie': 'hkfpwfaxeyr61sr9g69uw0jok57jzxj6u2a',
               'logGuid': 'de12958e-96fd-43a8-b6d0-fa838e829897',
               'new_search_uid': '973a8b4bacc9fd160fd25bf6e6e3971f',
               'unique_cookie': 'U_hkfpwfaxeyr61sr9g69uw0jok57jzxj6u2a*36'}

    def start_requests(self):
        urls = ['https://sz.newhouse.fang.com/house/s/', 'https://sz.esf.fang.com/?ctm=1.sz.xf_search.head.140']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=ftxHouse.cookies)

    def parse(self, response):
        url = response.url
        if ftxHouse.new_house_url == url:
            ftxHouse.new_house(self, response)
            # 新房下一页内容
            next_page = response.css('#sjina_C01_47 ul li.fr a.next::attr(href)').get()
            if not (next_page is None) | (str(next_page).startswith("http")) | (str(next_page).startswith("https")):
                next_page = ftxHouse.new_house_domain + next_page

            yield scrapy.Request(url=next_page, callback=self.parse, cookies=ftxHouse.cookies)
        elif ftxHouse.old_house_url == url:
            ftxHouse.old_house(self, response)
            # 二手房下一页内容
            next_page = response.css('#list_D10_15 p')[0].css('a::attr(href)').get()
            if not (next_page is None) | (str(next_page).startswith("http")) | (str(next_page).startswith("https")):
                next_page = ftxHouse.old_house_domain + next_page

            yield scrapy.Request(next_page, callback=self.parse, cookies=ftxHouse.cookies)

    def new_house(self, response):
        all_house_li = response.css('#newhouse_loupai_list ul')
        house_items = []
        for index, house_li in enumerate(all_house_li):
            try:
                house_dict = {}
                # 图片地址
                house_image = house_li.css('div.clearfix a img::attr(src)').get()
                house_dict['house_image'] = house_image
                # 房子名称
                house_name = house_li.css('div.nlc_details a::text').get()
                house_dict['house_name'] = house_name
                # 房子价格
                house_price = house_li.css('div.nlc_details div.nhouse_price')[index].get()
                house_dict['house_price'] = house_price
                # 房子地址
                house_address = house_li.css('div.nlc_details div.relative_message a::attr(title)').get()
                house_dict['house_address'] = house_address
                # 房子信息集合
                house_items.append(house_dict)
            except BaseException:
                print("获取新房信息异常，原因：", BaseException.__cause__)

        print("新房信息为", house_items)

    def old_house(self, response):
        all_house_dl = response.css('div.shop_list_4 dl')
        house_items = []

        for house_dl in all_house_dl:
            try:
                house_dict = {}
                # 房屋图片地址
                house_image = house_dl.css('dt a img::attr(src)').get()
                house_dict['house_image'] = house_image
                # 房屋基本信息 2室2厅 |78㎡ |高层（共28层） |南向 |2001年建
                house_base = house_dl.css('dd p.tel_shop::text').getall()
                house_dict['house_base'] = house_base
                # 房屋地址
                house_address = str(house_dl.css('dd p.add_shop a::attr(title)').get()) + str(
                    house_dl.css('dd p.add_shop span::text').get())
                house_dict['house_address'] = house_address
                # 满五优质教育业主急售黄金楼层距3号线华新站约176米
                house_other = house_dl.css('dd p.clearfix span::text').getall()
                house_dict['house_other'] = house_other
                # 房子价格
                house_price = house_dl.css('dd.price_right span.red b::text').get() + \
                              house_dl.css('dd.price_right span::text')[0].get()
                house_dict['house_price'] = house_price
                # 房子大小
                house_size = house_dl.css('dd.price_right span::text')[1].get()
                house_dict['house_size'] = house_size
                house_items.append(house_dict)
            except BaseException:
                print("二手房信息获取失败，原因为", BaseException.__cause__)

        print("二手房信息为", house_items)
