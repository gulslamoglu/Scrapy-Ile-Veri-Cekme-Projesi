import scrapy
import json

class PetlebiSpider(scrapy.Spider):
    name = 'petlebi'
    start_urls = [
        'https://www.petlebi.com/kedi-petshop-urunleri?page=1',
        'https://www.petlebi.com/kopek-petshop-urunleri?page=1',
        'https://www.petlebi.com/kus-petshop-urunleri?page=1',
        'https://www.petlebi.com/kemirgen-petshop-urunleri?page=1'
    ]

    def parse(self, response):
        total_pages = int(response.xpath('//ul[@class="pagination"]/li[last()-1]/a/text()').get())
        base_url = response.url.split('?')[0]

        for page_number in range(1, total_pages + 1):
            url = f"{base_url}?page={page_number}"
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        products = response.xpath('//*[@id="products"]/div')
        category = response.url.split('/')[-1]  # Kategoriyi URL'den al
        for product in products:
            item = {
                'kategori': category,
                'ürün URL\'si': product.xpath('.//a[@class="p-link"]/@href').get(),
                'ürün adı': product.xpath('.//a[@class="p-link"]/@title').get(),
                'ürün barkodu': product.xpath('.//a[@class="p-link"]/@id').get(),
                'ürün fiyatı': product.xpath('.//@data-gtm-product').re_first(r'"price":"([^"]+)"'),
                'ürün stoğu': self.extract_stock_info(product.xpath('.//@data-gtm-product').get()),
                'ürün resimleri': product.xpath('.//img/@data-original').get(),
                'açıklama': '',
                'sku': '',
                'kategori': product.xpath('.//@data-gtm-product').re_first(r'"category":"([^"]+)"'),
                'ürün kimlik': product.xpath('.//@data-gtm-product').re_first(r'"id":"([^"]+)"'),
                'marka': product.xpath('.//@data-gtm-product').re_first(r'"brand":"([^"]+)"'),

            }
            # Her ürün için ayrı bir HTTP isteği yaparak SKU, barkod ve açıklama bilgilerini almak
            product_url = product.xpath('.//a[@class="p-link"]/@href').get()
            if product_url:
                request = scrapy.Request(product_url, callback=self.parse_product)
                request.meta['item'] = item
                yield request

    def parse_product(self, response):
        item = response.meta['item']
        item['açıklama'] = response.xpath('//div[contains(@class, "tab-pane") and contains(@class, "read-more-box")]/span[@id="productDescription"]//text()').getall()
        item['sku'] = response.xpath('//span[@class="pdbestbefore"]/strong/text()').get()
        item['ürün barkodu'] = response.xpath('//div[@id="hakkinda"]/div[@class="row mb-2"]/div[@class="col-10 pd-d-v"]/text()').get()
        item['ürün stoğu'] = self.extract_stock_info(response.xpath('//*[@id="product291"]/@data-gtm-product').get())
        yield item

    def extract_stock_info(self, gtm_product_data):
        try:
            if gtm_product_data:
                json_data = json.loads(gtm_product_data)
                return json_data.get('dimension2')
            else:
                return "In Stock"
        except json.JSONDecodeError:
            return "Geçersiz JSON Formatı"
