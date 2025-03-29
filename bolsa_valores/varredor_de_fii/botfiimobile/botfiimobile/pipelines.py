# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
from botfiimobile.settings import XLSX_PATH

CAMPOS = ['Papel','Segmento','Dividend Yield','P/VP','Valor de Mercado','Liquidez','Link']
class BotfiimobilePipeline(object):
    planilha = None
    sheet = None

    def open_spider(self,spider):
        self.planilha = openpyxl.Workbook()
        self.sheet =self.planilha.active
        self.sheet.append(CAMPOS)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.sheet.append([adapter.get('Papel'),adapter.get('Segmento'),adapter.get('Dividend Yield'),adapter.get('P/VP'),adapter.get('Valor de Mercado'),adapter.get('Liquidez'),adapter.get('Link')])

        return item
    
    def close_spider(self,spider):
        self.planilha.save(XLSX_PATH)

