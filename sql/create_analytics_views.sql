USE sephora_analytics;


-- =========================================================
-- 1. MONTHLY REVENUE VIEW
-- =========================================================

DROP VIEW IF EXISTS vw_monthly_revenue;

CREATE VIEW vw_monthly_revenue AS

SELECT
    d.year,
    d.month,
    d.month_name,

    ROUND(
        SUM(f.net_revenue_inr),
        2
    ) AS revenue_inr,

    COUNT(DISTINCT f.order_id) AS total_orders,

    ROUND(
        SUM(f.net_revenue_inr)
        / COUNT(DISTINCT f.order_id),
        2
    ) AS average_order_value_inr

FROM fact_sales f

JOIN dim_date d
    ON f.date_id = d.date_id

GROUP BY
    d.year,
    d.month,
    d.month_name;


-- =========================================================
-- 2. CATEGORY PERFORMANCE VIEW
-- =========================================================

DROP VIEW IF EXISTS vw_category_performance;

CREATE VIEW vw_category_performance AS

SELECT

    p.category,

    COUNT(DISTINCT f.order_id)
        AS total_orders,

    SUM(f.quantity)
        AS units_sold,

    ROUND(
        SUM(f.net_revenue_inr),
        2
    ) AS revenue_inr,

    ROUND(
        AVG(f.net_revenue_inr),
        2
    ) AS avg_line_revenue_inr

FROM fact_sales f

JOIN dim_product p
    ON f.product_id = p.product_id

GROUP BY
    p.category;


-- =========================================================
-- 3. PRODUCT PERFORMANCE VIEW
-- =========================================================

DROP VIEW IF EXISTS vw_product_performance;

CREATE VIEW vw_product_performance AS

SELECT

    p.product_id,
    p.product_name,
    p.brand,
    p.category,

    COUNT(DISTINCT f.order_id)
        AS total_orders,

    SUM(f.quantity)
        AS units_sold,

    ROUND(
        SUM(f.net_revenue_inr),
        2
    ) AS revenue_inr,

    ROUND(
        AVG(f.discount_percent),
        2
    ) AS avg_discount_percent

FROM fact_sales f

JOIN dim_product p
    ON f.product_id = p.product_id

GROUP BY

    p.product_id,
    p.product_name,
    p.brand,
    p.category;


-- =========================================================
-- 4. CUSTOMER PERFORMANCE VIEW
-- =========================================================

DROP VIEW IF EXISTS vw_customer_performance;

CREATE VIEW vw_customer_performance AS

SELECT

    c.customer_id,
    c.first_name,
    c.last_name,
    c.loyalty_tier,

    COUNT(DISTINCT f.order_id)
        AS total_orders,

    SUM(f.quantity)
        AS total_units,

    ROUND(
        SUM(f.net_revenue_inr),
        2
    ) AS lifetime_value_inr,

    ROUND(
        SUM(f.net_revenue_inr)
        / COUNT(DISTINCT f.order_id),
        2
    ) AS customer_aov_inr

FROM fact_sales f

JOIN dim_customer c
    ON f.customer_id = c.customer_id

GROUP BY

    c.customer_id,
    c.first_name,
    c.last_name,
    c.loyalty_tier;


-- =========================================================
-- 5. STORE PERFORMANCE VIEW
-- =========================================================

DROP VIEW IF EXISTS vw_store_performance;

CREATE VIEW vw_store_performance AS

SELECT

    s.store_id,
    s.store_name,
    s.city,
    s.area,

    COUNT(DISTINCT f.order_id)
        AS total_orders,

    SUM(f.quantity)
        AS units_sold,

    ROUND(
        SUM(f.net_revenue_inr),
        2
    ) AS revenue_inr,

    ROUND(
        SUM(f.net_revenue_inr)
        / COUNT(DISTINCT f.order_id),
        2
    ) AS average_order_value_inr

FROM fact_sales f

JOIN dim_store s
    ON f.store_id = s.store_id

WHERE
    f.channel = 'Physical Store'

GROUP BY

    s.store_id,
    s.store_name,
    s.city,
    s.area;


-- =========================================================
-- 6. CHANNEL PERFORMANCE VIEW
-- =========================================================

DROP VIEW IF EXISTS vw_channel_performance;

CREATE VIEW vw_channel_performance AS

SELECT

    channel,

    COUNT(DISTINCT order_id)
        AS total_orders,

    SUM(quantity)
        AS units_sold,

    ROUND(
        SUM(net_revenue_inr),
        2
    ) AS revenue_inr,

    ROUND(
        SUM(net_revenue_inr)
        / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value_inr

FROM fact_sales

GROUP BY channel;