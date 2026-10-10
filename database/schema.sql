-- E-Commerce Database Schema (SQLite / DuckDB Compatible) - Indian Marketplace

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    signup_date DATE,
    customer_segment VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    unit_price DECIMAL(12, 2),
    cost_price DECIMAL(12, 2),
    stock_quantity INT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_date TIMESTAMP,
    payment_method VARCHAR(50),
    shipping_city VARCHAR(100),
    order_status VARCHAR(30),
    total_amount DECIMAL(14, 2)
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(12, 2),
    discount_amount DECIMAL(12, 2),
    total_price DECIMAL(14, 2)
);

CREATE TABLE IF NOT EXISTS web_clickstream (
    event_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    session_id VARCHAR(50),
    event_type VARCHAR(30),
    page_url VARCHAR(255),
    event_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rfm_segments (
    customer_id VARCHAR(50) PRIMARY KEY,
    recency INT,
    frequency INT,
    monetary DECIMAL(14, 2),
    r_score INT,
    f_score INT,
    m_score INT,
    rfm_cell VARCHAR(10),
    segment VARCHAR(50),
    calculated_at TIMESTAMP
);
