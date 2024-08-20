CREATE TABLE petlebi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255),
    name VARCHAR(255),
    barcode VARCHAR(50),
    price DECIMAL(10, 2),
    stock VARCHAR(50),
    images TEXT,
    description TEXT,
    sku VARCHAR(50),
    category VARCHAR(255),
    product_id INT,
    brand VARCHAR(255)
);
