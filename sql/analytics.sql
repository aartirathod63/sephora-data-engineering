USE sephora_analytics;


-- =========================================================
-- 1. TOTAL REVENUE
-- =========================================================

SELECT
    ROUND(SUM(net_revenue_inr), 2) AS total_revenue_inr
FROM fact_sales;


-- =========================================================
-- 2. TOTAL ORDERS
-- =========================================================

SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM fact_sales;


-- =========================================================
-- 3. AVERAGE ORDER VALUE
-- =========================================================

SELECT
    ROUND(
        SUM(order_revenue) / COUNT(*),
        2
    ) AS average_order_value_inr
FROM (
    SELECT
        order_id,
        SUM(net_revenue_inr) AS order_revenue
    FROM fact_sales
    GROUP BY order_id
) t;


-- =========================================================
-- 4. REVENUE BY CATEGORY
-- =========================================================

SELECT
    p.category,
    ROUND(SUM(f.net_revenue_inr), 2) AS revenue_inr
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue_inr DESC;


-- =========================================================
-- 5. TOP 10 PRODUCTS BY REVENUE
-- =========================================================

SELECT
    p.product_id,
    p.product_name,
    p.brand,
    p.category,
    ROUND(SUM(f.net_revenue_inr), 2) AS revenue_inr
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.brand,
    p.category
ORDER BY revenue_inr DESC
LIMIT 10;


-- =========================================================
-- 6. TOP 10 BRANDS
-- =========================================================

SELECT
    p.brand,
    ROUND(SUM(f.net_revenue_inr), 2) AS revenue_inr
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.brand
ORDER BY revenue_inr DESC
LIMIT 10;


-- =========================================================
-- 7. REVENUE BY CHANNEL
-- =========================================================

SELECT
    channel,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(net_revenue_inr), 2) AS revenue_inr
FROM fact_sales
GROUP BY channel
ORDER BY revenue_inr DESC;


-- =========================================================
-- 8. REVENUE BY LOYALTY TIER
-- =========================================================

SELECT
    c.loyalty_tier,
    COUNT(DISTINCT f.order_id) AS orders,
    ROUND(SUM(f.net_revenue_inr), 2) AS revenue_inr
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY c.loyalty_tier
ORDER BY revenue_inr DESC;


-- =========================================================
-- 9. TOP 10 CUSTOMERS
-- =========================================================

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.loyalty_tier,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.net_revenue_inr), 2) AS lifetime_value_inr
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.loyalty_tier
ORDER BY lifetime_value_inr DESC
LIMIT 10;


-- =========================================================
-- 10. MONTHLY REVENUE
-- =========================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.net_revenue_inr), 2) AS revenue_inr
FROM fact_sales f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- =========================================================
-- 11. STORE PERFORMANCE
-- =========================================================

SELECT
    s.store_name,
    s.city,
    s.area,
    COUNT(DISTINCT f.order_id) AS orders,
    ROUND(SUM(f.net_revenue_inr), 2) AS revenue_inr
FROM fact_sales f
JOIN dim_store s
    ON f.store_id = s.store_id
WHERE f.channel = 'Physical Store'
GROUP BY
    s.store_id,
    s.store_name,
    s.city,
    s.area
ORDER BY revenue_inr DESC;


-- =========================================================
-- 12. REPEAT VS ONE-TIME CUSTOMERS
-- =========================================================

WITH customer_orders AS (

    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM fact_sales
    GROUP BY customer_id

)

SELECT
    CASE
        WHEN order_count = 1
            THEN 'One-Time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,

    COUNT(*) AS customers

FROM customer_orders

GROUP BY customer_type;


-- =========================================================
-- 13. CATEGORY MARKET SHARE
-- =========================================================

SELECT
    p.category,

    ROUND(
        SUM(f.net_revenue_inr) * 100.0
        /
        (
            SELECT SUM(net_revenue_inr)
            FROM fact_sales
        ),
        2
    ) AS revenue_share_percent

FROM fact_sales f

JOIN dim_product p
    ON f.product_id = p.product_id

GROUP BY p.category

ORDER BY revenue_share_percent DESC;


-- =========================================================
-- 14. ONLINE VS PHYSICAL STORE AOV
-- =========================================================

SELECT
    channel,

    ROUND(
        SUM(order_revenue)
        /
        COUNT(*),
        2
    ) AS average_order_value_inr

FROM (

    SELECT
        order_id,
        channel,
        SUM(net_revenue_inr) AS order_revenue

    FROM fact_sales

    GROUP BY
        order_id,
        channel

) t

GROUP BY channel;


-- =========================================================
-- 15. DISCOUNT IMPACT
-- =========================================================

SELECT

    CASE
        WHEN discount_percent = 0
            THEN 'No Discount'
        WHEN discount_percent <= 10
            THEN '1-10%'
        WHEN discount_percent <= 20
            THEN '11-20%'
        ELSE '20%+'
    END AS discount_band,

    COUNT(*) AS line_items,

    ROUND(
        SUM(net_revenue_inr),
        2
    ) AS revenue_inr

FROM fact_sales

GROUP BY discount_band

ORDER BY revenue_inr DESC;