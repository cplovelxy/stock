import logging
import os
import re

import scrapy
import xlwt

from .export import export


class ftxHouse(scrapy.Spider):
    new_house_dict = {'last': ''}
    old_house_dict = {'last': ''}
    name = 'ftx_house'
    new_house_url = 'https://sz.newhouse.fang.com/house/s/'
    old_house_url = 'https://sz.esf.fang.com/house/'
    new_house_array_message = []
    old_house_array_message = []
    new_house_cookies = {'city': 'sz', 'global_cookie': 'hkfpwfaxeyr61sr9g69uw0jok57jzxj6u2a',
                         'Integrateactivity': 'notincludemc', 'new_search_uid': '973a8b4bacc9fd160fd25bf6e6e3971f',
                         '__utmz': '147393320.1567156397.3.3.utmcsr=sz.newhouse.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/house/s/b92/',
                         '__utma': '147393320.125060648.1567134119.1567159658.1570609344.5',
                         '__utmc': '147393320', '__utmt_t0': '1', '__utmt_t1': '1', '__utmt_t2': '1', '__utmt_t3': '1',
                         '__utmt_t4': '1', 'newhouse_user_guid': '057B5A2E-4AAF-CD59-D0AA-23765413F811',
                         'newhouse_chat_guid': '3EED06BD-5B99-3FA7-496C-3833CA368283',
                         'newhouse_ac1': '1_1570609495_2740%5B%3A%7C%40%7C%3A%5D06b5bec6129a5ded2ff6906118ee5814',
                         'Captcha': '2F45686D784E733762716E4A577A2B676A755A2F70353762433652516E422B6263797747392F68486D534272646D577761425641436B4E66544B6C48676776684C6C37394B714B6D7A52553D',
                         'g_sourcepage': 'xf_lp%5Elb_pc', 'unique_cookie': 'U_l77ozn5i48sj14cv3g9w3lfb12uk1j08zgo*14',
                         '__utmb': '147393320.20.10.1570609344'}
    new_house_headers = {':authority': 'sz.newhouse.fang.com', ':method': 'GET', ':path': '/house/s/',
                         ':scheme': 'https',
                         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                         'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9',
                         'cache-control': 'max-age=0', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none',
                         'sec-fetch-user': '?1',
                         'upgrade-insecure-requests': '1',
                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    old_house_cookies = {'city': 'sz', 'global_cookie': 'hkfpwfaxeyr61sr9g69uw0jok57jzxj6u2a',
                         'Integrateactivity': 'notincludemc', 'new_search_uid': '973a8b4bacc9fd160fd25bf6e6e3971f',
                         '__utmz': '147393320.1570870808.8.5.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-ac86c4813f4287385f/redirect',
                         '__utma': '147393320.125060648.1567134119.1567159658.1570609344.5',
                         '__utmc': '147393320', '__utmt_t0': '1', '__utmt_t1': '1', '__utmt_t2': '1', '__utmt_t3': '1',
                         '__utmt_t4': '1', 'newhouse_user_guid': '057B5A2E-4AAF-CD59-D0AA-23765413F811',
                         'newhouse_chat_guid': '3EED06BD-5B99-3FA7-496C-3833CA368283',
                         'newhouse_ac1': '1_1570609495_2740%5B%3A%7C%40%7C%3A%5D06b5bec6129a5ded2ff6906118ee5814',
                         'Captcha': '2F45686D784E733762716E4A577A2B676A755A2F70353762433652516E422B6263797747392F68486D534272646D577761425641436B4E66544B6C48676776684C6C37394B714B6D7A52553D',
                         'logGuid': 'ee403ce3-c692-4975-b43d-751214b9171f',
                         'g_sourcepage': 'ehlist', 'unique_cookie': 'U_l77ozn5i48sj14cv3g9w3lfb12uk1j08zgo*63',
                         '__utmb': '147393320.248.10.1570609344'}

    old_house_headers = {':authority': 'sz.esf.fang.com', ':method': 'GET', ':path': '/house/i31',
                         ':scheme': 'https',
                         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                         'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9',
                         'cache-control': 'max-age=0', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-site',
                         'sec-fetch-user': '?1',
                         'upgrade-insecure-requests': '1',
                         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    def start_requests(self):
        urls = ['https://sz.newhouse.fang.com/house/s/b91', 'https://sz.esf.fang.com/house/i31']
        for url in urls:
            if url.startswith(ftxHouse.new_house_url):
                yield scrapy.Request(url=url, callback=self.parse, cookies=ftxHouse.new_house_cookies,
                                     headers=ftxHouse.new_house_headers)
            else:
                yield scrapy.Request(url=url, callback=self.parse, cookies=ftxHouse.old_house_cookies,
                                     headers=ftxHouse.old_house_headers)

    def parse(self, response):
        url = response.url

        if str(url).startswith(ftxHouse.new_house_url):
            page_number = str(int(str(url).split('b9')[1].replace("/", '')) + 1)
            next_page = ftxHouse.new_house_url + 'b9' + page_number
            print('获取到的下一页的链接为' + str(next_page))
            # 首次初始化尾页页码是多少
            if ftxHouse.new_house_dict.get('last') == '':
                last_url = response.css('#sjina_C01_47 ul li.fr a.last::attr(href)').get()
                ftxHouse.new_house_dict['last'] = str(int(str(last_url).split('b9')[1].replace("/", '')))
            # 判断有没有到达尾页
            if int(ftxHouse.new_house_dict.get('last')) < int(page_number):
                ftxHouse.export_new_house()
                return
            # 解析数据
            ftxHouse.new_house(self, response)
            if not (next_page is None):
                yield scrapy.Request(url=next_page, callback=self.parse,
                                     cookies=ftxHouse.new_house_cookies,
                                     headers=ftxHouse.new_house_headers)

        else:
            old_house_redirect_url = response.css('div.redirect a::attr(href)').get()
            old_house_next_page = old_house_redirect_url
            if not (old_house_redirect_url is None):
                print("获取到的二手房重定向的链接为" + str(old_house_next_page))
                yield scrapy.Request(url=str(old_house_next_page), callback=self.parse,
                                     cookies=ftxHouse.old_house_cookies,
                                     headers=ftxHouse.old_house_headers)
            else:
                if ftxHouse.old_house_dict.get('last') == '':
                    # 这里如果报错需要去房添加去输入图片验证码
                    try:
                        last_url = response.css('#list_D10_15 p a::attr(href)')[1].get()
                        ftxHouse.old_house_dict['last'] = str(int(str(last_url).split('i3')[1].replace("/", '')))
                    except Exception as e:
                        logging.error('爬取房天下二手房信息需要图片验证码，请前往', response.url, '验证')
                page_number = int(int(re.sub(r"\?.*", "", str(response.url).split('i3')[1])) + 1)
                if int(ftxHouse.old_house_dict.get('last')) < page_number:
                    logging.info("爬二手房信息结束，当前页码为", page_number)
                    ftxHouse.export_old_house()
                    return

                ftxHouse.old_house(self, response)
                next_page = ftxHouse.old_house_url + 'i3' + str(page_number)
                print("获取到的二手房下一页的链接为", next_page)
                yield scrapy.Request(url=next_page, callback=self.parse,
                                     cookies=ftxHouse.old_house_cookies,
                                     headers=ftxHouse.old_house_headers)

    def new_house(self, response):
        all_house_li = response.css('#newhouse_loupai_list ul')
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
                house_price = house_li.css('div.nlc_details div.nhouse_price span::text').get() + \
                              house_li.css('div.nlc_details div.nhouse_price em::text').get()
                house_dict['house_price'] = house_price
                # 房子地址
                house_address = house_li.css('div.nlc_details div.relative_message a::attr(title)').get()
                house_dict['house_address'] = house_address
                # 房子信息集合
                ftxHouse.new_house_array_message.append(house_dict)
            except BaseException as e:
                logging.info("获取新房信息异常，原因：", e)

    def old_house(self, response):
        all_house_dl = response.css('div.shop_list_4 dl')
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
                house_dict['house_other_message'] = house_other
                # 房子总价
                house_price = house_dl.css('dd.price_right span.red b::text').get() + \
                              house_dl.css('dd.price_right span::text')[0].get()
                house_dict['house_amount_price'] = house_price
                # 房子单价
                house_unit_price = house_dl.css('dd.price_right span::text')[1].get()
                house_dict['house_unit_price'] = house_unit_price

                # 房子面积'63.2㎡                                            '
                if str(house_base[1]).rfind('㎡') != -1:
                    house_dict['house_size'] = house_base[1]
                else:
                    logging.info(house_base)
                    house_dict['house_size'] = house_base[3]

                ftxHouse.old_house_array_message.append(house_dict)
            except Exception as e:
                logging.info("二手房信息获取失败，原因为", e)

    @staticmethod
    def export_new_house():
        new_house_file_path = str(export.export_path()) + os.path.sep + 'ftx_new_house.xls'
        new_house_header = ['house_image', 'house_name', 'house_price', 'house_address']
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('new_house', cell_overwrite_ok=False)
        i = 0
        for k in new_house_header:
            sheet.write(0, i, k)
            i = i + 1
        row = 1
        for new_house_message in ftxHouse.new_house_array_message:
            sheet.write(row, 0, new_house_message['house_image'])
            sheet.write(row, 1, new_house_message['house_name'])
            sheet.write(row, 2, new_house_message['house_price'])
            sheet.write(row, 3, new_house_message['house_address'])
            row = row + 1
        book.save(new_house_file_path)

    @staticmethod
    def export_old_house():
        old_house_file_path = str(export.export_path()) + os.path.sep + 'ftx_old_house.xls'
        old_house_header = ['house_image', 'house_base', 'house_address', 'house_other_message', 'house_amount_price',
                            'house_unit_price', 'house_size']
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('old_house', cell_overwrite_ok=False)
        i = 0
        for k in old_house_header:
            sheet.write(0, i, k)
            i = i + 1
        row = 1
        for old_house_message in ftxHouse.old_house_array_message:
            sheet.write(row, 0, old_house_message['house_image'])
            sheet.write(row, 1, old_house_message['house_base'])
            sheet.write(row, 2, old_house_message['house_address'])
            sheet.write(row, 3, old_house_message['house_other_message'])
            sheet.write(row, 4, old_house_message['house_amount_price'])
            sheet.write(row, 5, old_house_message['house_unit_price'])
            sheet.write(row, 6, old_house_message['house_size'])
            row = row + 1
        book.save(old_house_file_path)
