from scrapy.exporters import CsvItemExporter
from scrapy.loader import ItemLoader
from ..house.item.new_house_item import NewHouse

class houseUtils(object):

    def export_item(self, response):
        it = ItemLoader(item=NewHouse(), response=response)
        it.add_css('house_image', '#newhouse_loupai_list ul div.clearfix a img::attr(src)')
        it.add_css('house_name', '#newhouse_loupai_list ul div.nlc_details a::text')
        it.add_css('house_price', '#newhouse_loupai_list ul div.nlc_details div.nhouse_price')
        it.add_css('house_address', '#newhouse_loupai_list ul div.nlc_details div.relative_message a::attr(title)')
        it.load_item()

        old_house_dict_header = {'house_image', 'house_name', 'house_price', 'house_address'}
        csvItemExporter = CsvItemExporter('ftx_old_house', old_house_dict_header)
        csvItemExporter.export_item(it.item)
