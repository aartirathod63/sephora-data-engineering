CREATE DATABASE IF NOT EXISTS sephora_analytics;

USE sephora_analytics;


-- =========================================================
-- DIMENSION: CUSTOMER
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_customer (

    customer_id VARCHAR(20) PRIMARY KEY,

    first_name VARCHAR(100),

    last_name VARCHAR(100),

    email VARCHAR(255),

    city VARCHAR(100),

    state VARCHAR(100),

    age INT,

    gender VARCHAR(30),

    signup_date DATE,

    loyalty_tier VARCHAR(30)

);


-- =========================================================
-- DIMENSION: PRODUCT
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_product (

    product_id VARCHAR(20) PRIMARY KEY,

    product_name VARCHAR(255),

    brand VARCHAR(100),

    category VARCHAR(100),

    subcategory VARCHAR(100),

    mrp_inr DECIMAL(10,2),

    rating DECIMAL(3,2),

    review_count INT,

    size VARCHAR(50),

    stock_quantity INT

);


-- =========================================================
-- DIMENSION: STORE
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_store (

    store_id VARCHAR(20) PRIMARY KEY,

    store_name VARCHAR(255),

    city VARCHAR(100),

    state VARCHAR(100),

    mall VARCHAR(255),

    area VARCHAR(100),

    store_type VARCHAR(100)

);


-- =========================================================
-- DIMENSION: DATE
-- =========================================================

CREATE TABLE IF NOT EXISTS dim_date (

    date_id INT PRIMARY KEY,

    full_date DATE UNIQUE,

    year INT,

    quarter INT,

    month INT,

    month_name VARCHAR(20),

    day INT,

    day_name VARCHAR(20),

    week INT

);


-- =========================================================
-- FACT: SALES
-- =========================================================

CREATE TABLE IF NOT EXISTS fact_sales (

    order_item_id VARCHAR(30) PRIMARY KEY,

    order_id VARCHAR(30) NOT NULL,

    customer_id VARCHAR(20) NOT NULL,

    product_id VARCHAR(20) NOT NULL,

    store_id VARCHAR(20),

    date_id INT,

    channel VARCHAR(50),

    payment_method VARCHAR(50),

    order_status VARCHAR(50),

    quantity INT,

    unit_price_inr DECIMAL(10,2),

    discount_percent DECIMAL(5,2),

    discount_amount_inr DECIMAL(10,2),

    gross_amount_inr DECIMAL(12,2),

    net_revenue_inr DECIMAL(12,2),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    FOREIGN KEY (store_id)
        REFERENCES dim_store(store_id),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)

);


-- =========================================================
-- INDEXES
-- =========================================================

CREATE INDEX idx_fact_order
ON fact_sales(order_id);

CREATE INDEX idx_fact_customer
ON fact_sales(customer_id);

CREATE INDEX idx_fact_product
ON fact_sales(product_id);

CREATE INDEX idx_fact_store
ON fact_sales(store_id);

CREATE INDEX idx_fact_date
ON fact_sales(date_id);

CREATE INDEX idx_fact_channel
ON fact_sales(channel);
