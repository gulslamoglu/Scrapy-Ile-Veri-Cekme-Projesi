import mysql.connector
import json

# JSON dosyasından verileri oku
def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# MySQL veritabanına bağlan
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="gulislamoglu",
            password="Gul081832.",
            database="yeni_veritabani"
        )
        return conn
    except mysql.connector.Error as err:
        print("MySQL Error: {}".format(err))
        return None

# Verileri MySQL veritabanına ekle
def import_data_to_mysql(data, conn):
    def stringify_description(description_list):
        if isinstance(description_list, list):
            return ' '.join(description_list).strip()
        else:
            return str(description_list)

    if conn is not None:
        cursor = conn.cursor()
        try:
            for item in data:
                query = """
                INSERT INTO petlebi (url, name, barcode, price, stock, images, description, sku, category, product_id, brand)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    item['ürün URL\'si'], 
                    item['ürün adı'], 
                    item['ürün barkodu'], 
                    item['ürün fiyatı'], 
                    item['ürün stoğu'], 
                    item['ürün resimleri'], 
                    stringify_description(item['açıklama']),  # açıklama alanını dönüştür
                    item['sku'], 
                    item['kategori'], 
                    item['ürün kimlik'], 
                    item['marka']
                )
                #print("values:", values)  # Burada values değişkenini yazdırıyoruz
                cursor.execute(query, values)
            conn.commit()
            print("Veriler başarıyla eklendi.")
        except mysql.connector.Error as err:
            print("MySQL Error: {}".format(err))
        finally:
            cursor.close()
            conn.close()
    else:
        print("MySQL veritabanına bağlanılamadı.")

# Ana fonksiyon
def main():
    json_filename = 'petlebi_products.json'
    data = read_json(json_filename)
    conn = connect_to_mysql()
    import_data_to_mysql(data, conn)

if __name__ == "__main__":
    main()
