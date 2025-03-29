import scrapy
import random

class FiimobbotSpider(scrapy.Spider):
    name = 'fiimobbot'
    allowed_domains = ['fundamentus.com.br']
    start_urls = ['https://www.fundamentus.com.br/fii_resultado.php']

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        # Adicione mais user-agents aqui
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': random.uniform(1, 3), # Delay aleatório entre 1 e 3 segundos
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={'User-Agent': random.choice(self.user_agents)})

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_data, dont_filter=True, headers={'User-Agent': random.choice(self.user_agents)})

    def parse_data(self, response):
        for linha in response.xpath("//table[@id='tabelaResultado']//tr[position() > 1]"): #pula o cabeçalho
            yield {
                'Papel': linha.xpath('./td[1]//a/text()').get(default='N/A'),
                'Segmento': linha.xpath('./td[2]/text()').get(default='N/A'),
                'Dividend Yield': linha.xpath('./td[5]/text()').get(default='N/A'),
                'P/VP': linha.xpath('./td[6]/text()').get(default='N/A'),
                'Valor de Mercado': linha.xpath('./td[7]/text()').get(default='N/A'),
                'Liquidez': linha.xpath('./td[8]/text()').get(default='N/A'),
                'Link' : 'https://www.fundamentus.com.br/' + linha.xpath('.//a/@href').get(default='N/A')
            }