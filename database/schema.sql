-- =========================================
-- Autonomous E-Commerce Operations Agent
-- Database Schema - Olist Dataset
-- =========================================

-- إنشاء المخططات
CREATE SCHEMA IF NOT EXISTS stg;   -- البيانات الخام
CREATE SCHEMA IF NOT EXISTS mart;  -- البيانات النظيفة

-- =========================================
-- الجداول النهائية (Mart Layer)
-- =========================================

CREATE TABLE mart.customers (
    customer_id              TEXT PRIMARY KEY,
    customer_unique_id       TEXT NOT NULL,
    customer_zip_code_prefix TEXT,
    customer_city            TEXT,
    customer_state           CHAR(2)
);

CREATE TABLE mart.orders (
    order_id                      TEXT PRIMARY KEY,
    customer_id                   TEXT NOT NULL REFERENCES mart.customers(customer_id),
    order_status                  TEXT,
    order_purchase_timestamp      TIMESTAMP,
    order_approved_at             TIMESTAMP,
    order_delivered_carrier_date  TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE mart.products (
    product_id                 TEXT PRIMARY KEY,
    product_category_name      TEXT,
    product_name_length        SMALLINT,
    product_description_length SMALLINT,
    product_photos_qty         SMALLINT,
    product_weight_g           INTEGER,
    product_length_cm          SMALLINT,
    product_height_cm          SMALLINT,
    product_width_cm           SMALLINT
);

CREATE TABLE mart.sellers (
    seller_id              TEXT PRIMARY KEY,
    seller_zip_code_prefix TEXT,
    seller_city            TEXT,
    seller_state           CHAR(2)
);

CREATE TABLE mart.order_items (
    order_id            TEXT NOT NULL REFERENCES mart.orders(order_id),
    order_item_id       SMALLINT NOT NULL,
    product_id          TEXT REFERENCES mart.products(product_id),
    seller_id           TEXT REFERENCES mart.sellers(seller_id),
    shipping_limit_date TIMESTAMP,
    price               NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    freight_value       NUMERIC(10,2) NOT NULL CHECK (freight_value >= 0),
    PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE mart.order_payments (
    order_id             TEXT NOT NULL REFERENCES mart.orders(order_id),
    payment_sequential   SMALLINT NOT NULL,
    payment_type         TEXT,
    payment_installments SMALLINT,
    payment_value        NUMERIC(12,2),
    PRIMARY KEY (order_id, payment_sequential)
);

CREATE TABLE mart.order_reviews (
    review_id               TEXT PRIMARY KEY,
    order_id                TEXT NOT NULL REFERENCES mart.orders(order_id),
    review_score            SMALLINT CHECK (review_score BETWEEN 1 AND 5),
    review_comment_title    TEXT,
    review_comment_message  TEXT,
    review_creation_date    TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);

CREATE TABLE mart.geolocation (
    geolocation_zip_code_prefix TEXT,
    geolocation_lat             NUMERIC(9,6),
    geolocation_lng             NUMERIC(9,6),
    geolocation_city            TEXT,
    geolocation_state           CHAR(2)
);

CREATE TABLE mart.category_translation (
    product_category_name         TEXT PRIMARY KEY,
    product_category_name_english TEXT
);

-- =========================================
-- الفهارس لتسريع استعلامات الـ Agent
-- =========================================
CREATE INDEX idx_orders_customer    ON mart.orders(customer_id);
CREATE INDEX idx_orders_status      ON mart.orders(order_status);
CREATE INDEX idx_orders_purchase_ts ON mart.orders(order_purchase_timestamp);
CREATE INDEX idx_items_product      ON mart.order_items(product_id);
CREATE INDEX idx_items_seller       ON mart.order_items(seller_id);
CREATE INDEX idx_reviews_order      ON mart.order_reviews(order_id);
CREATE INDEX idx_payments_order     ON mart.order_payments(order_id);
CREATE INDEX idx_geo_zip            ON mart.geolocation(geolocation_zip_code_prefix);
