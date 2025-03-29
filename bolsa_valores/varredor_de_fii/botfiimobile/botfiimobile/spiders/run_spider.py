import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Fbotfiimobile.spiders.fiimobbot import fiimobbot  # Substitua com o nome correto do seu projeto e spider

process = CrawlerProcess(get_project_settings())
process.crawl(fiimobbot)
process.start('fundos imobiliarios.xlsx')