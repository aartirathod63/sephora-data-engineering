USE sephora_analytics;


-- =========================================================
-- 1. RANK PRODUCTS WITHIN EACH CATEGORY
-- =========================================================

WITH product_revenue AS (

    SELECT
        p.category,
        p.product_id,
        p.product_name,
        p.brand,

        ROUND(
            SUM(f.net_revenue_inr),
            2
        ) AS revenue_inr

    FROM fact_sales f

    JOIN dim_product p
        ON f.product_id = p.product_id

    GROUP BY
        p.category,
        p.product_id,
        p.product_name,
        p.brand
),

ranked_products AS (

    SELECT

        category,
        product_id,
        product_name,
        brand,
        revenue_inr,

        RANK() OVER (
            PARTITION BY category
            ORDER BY revenue_inr DESC
        ) AS category_rank

    FROM product_revenue
)

SELECT *
FROM ranked_products
WHERE category_rank <= 3
ORDER BY
    category,
    category_rank;


-- =========================================================
-- 2. RUNNING MONTHLY REVENUE
-- =========================================================

WITH monthly_revenue AS (

    SELECT

        d.year,
        d.month,
        d.month_name,

        SUM(f.net_revenue_inr)
            AS revenue_inr

    FROM fact_sales f

    JOIN dim_date d
        ON f.date_id = d.date_id

    GROUP BY
        d.year,
        d.month,
        d.month_name
)

SELECT

    year,
    month,
    month_name,

    ROUND(
        revenue_inr,
        2
    ) AS monthly_revenue_inr,

    ROUND(
        SUM(revenue_inr) OVER (
            ORDER BY year, month
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS cumulative_revenue_inr

FROM monthly_revenue

ORDER BY
    year,
    month;


-- =========================================================
-- 3. MONTH-OVER-MONTH REVENUE GROWTH
-- =========================================================

WITH monthly_revenue AS (

    SELECT

        d.year,
        d.month,
        d.month_name,

        SUM(f.net_revenue_inr)
            AS revenue_inr

    FROM fact_sales f

    JOIN dim_date d
        ON f.date_id = d.date_id

    GROUP BY
        d.year,
        d.month,
        d.month_name
),

revenue_with_previous AS (

    SELECT

        year,
        month,
        month_name,
        revenue_inr,

        LAG(revenue_inr) OVER (
            ORDER BY year, month
        ) AS previous_month_revenue

    FROM monthly_revenue
)

SELECT

    year,
    month,
    month_name,

    ROUND(
        revenue_inr,
        2
    ) AS revenue_inr,

    ROUND(
        previous_month_revenue,
        2
    ) AS previous_month_revenue,

    ROUND(
        (
            revenue_inr
            - previous_month_revenue
        )
        * 100.0
        /
        NULLIF(
            previous_month_revenue,
            0
        ),
        2
    ) AS mom_growth_percent

FROM revenue_with_previous

ORDER BY
    year,
    month;