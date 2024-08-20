import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('petlebi_products.json', 'w', encoding='utf-8')
        self.file.write("[\n")

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(line)
        self.file.write(",\n") 
        return item
