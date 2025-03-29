import scrapy
import random
import pandas as pd

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

    def selecionar_melhores_fundos(self, dados):
        """Seleciona os 50 melhores fundos com base nos critérios especificados."""
        fundos_filtrados = dados[
            (dados['Dividend Yield'] >= 7.5) & (dados['Dividend Yield'] <= 14.5) &
            (dados['P/VP'] >= 0.85) & (dados['P/VP'] <= 1.1) &
            (dados['Valor de Mercado'] > 1000000000) &  # 1 bilhão
            (dados['Liquidez'] > 1000000)  # 1 milhão
        ]
        fundos_ordenados = fundos_filtrados.sort_values(by='Dividend Yield', ascending=False)
        top_50_fundos = fundos_ordenados.head(50)
        return top_50_fundos

    def parse_data(self, response):
        dados = []
        for linha in response.xpath("//table[@id='tabelaResultado']//tr[position() > 1]"):
            dados.append({
                'Papel': linha.xpath('./td[1]//a/text()').get(default='N/A'),
                'Segmento': linha.xpath('./td[2]/text()').get(default='N/A'),
                'Dividend Yield': linha.xpath('./td[5]/text()').get(default='N/A').replace('%', '').replace(',', '.'),
                'P/VP': linha.xpath('./td[6]/text()').get(default='N/A').replace(',', '.'),
                'Valor de Mercado': linha.xpath('./td[7]/text()').get(default='N/A').replace('R$', '').replace('.', '').replace(',', '.'),
                'Liquidez': linha.xpath('./td[8]/text()').get(default='N/A').replace('.', '').replace(',', '.'),
                'Link': 'https://www.fundamentus.com.br/' + linha.xpath('.//a/@href').get(default='N/A')
            })

        df = pd.DataFrame(dados)

        # Converter colunas numéricas para float
        df['Dividend Yield'] = pd.to_numeric(df['Dividend Yield'], errors='coerce')
        df['P/VP'] = pd.to_numeric(df['P/VP'], errors='coerce')
        df['Valor de Mercado'] = pd.to_numeric(df['Valor de Mercado'], errors='coerce')
        df['Liquidez'] = pd.to_numeric(df['Liquidez'], errors='coerce')

        # Remover linhas com valores NaN após a conversão
        df = df.dropna()

        # Selecionar os 50 melhores fundos
        top_50 = self.selecionar_melhores_fundos(df)

        # Converter DataFrame de volta para itens do Scrapy
        for index, row in top_50.iterrows():
            yield row.to_dict()