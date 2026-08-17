from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    when,
    to_date,
    date_format,
)


# =========================================================
# Spark
# =========================================================

spark = (
    SparkSession.builder
    .appName("SephoraFactSalesLoader")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


print("=" * 70)
print("SEPHORA FACT SALES LOADER")
print("=" * 70)


# =========================================================
# MySQL
# =========================================================

MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "sephora_analytics"
MYSQL_USER = "root"

# PUT YOUR MYSQL PASSWORD HERE
MYSQL_PASSWORD = "Aarti@123"


JDBC_URL = (
    f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/"
    f"{MYSQL_DATABASE}"
    "?useSSL=false"
    "&allowPublicKeyRetrieval=true"
    "&serverTimezone=Asia/Kolkata"
)


JDBC_PROPERTIES = {
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "driver": "com.mysql.cj.jdbc.Driver",
}


# =========================================================
# Read Raw Data
# =========================================================

print("\n===== READING ORDERS =====")

orders = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/orders.csv")
)


print("\n===== READING ORDER ITEMS =====")

order_items = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/raw/order_items.csv")
)


print("Orders:", orders.count())
print("Order Items:", order_items.count())


# =========================================================
# Build Fact
# =========================================================

print("\n===== BUILDING FACT_SALES =====")


fact_sales = (
    order_items.alias("oi")

    .join(
        orders.alias("o"),
        col("oi.order_id") == col("o.order_id"),
        "inner"
    )

    # Online orders don't belong to a physical store.
    # Therefore store_id becomes NULL.
    .withColumn(
        "warehouse_store_id",
        when(
            col("o.channel") == "Online",
            None
        ).otherwise(
            col("o.store_id")
        )
    )

    .select(

        col("oi.order_item_id"),

        col("o.order_id"),

        col("o.customer_id"),

        col("oi.product_id"),

        col("warehouse_store_id")
        .alias("store_id"),

        date_format(
            to_date(col("o.order_date")),
            "yyyyMMdd"
        )
        .cast("int")
        .alias("date_id"),

        col("o.channel"),

        col("o.payment_method"),

        col("o.order_status"),

        col("oi.quantity"),

        col("oi.unit_price_inr"),

        col("oi.discount_percent"),

        col("oi.discount_amount_inr"),

        (
            col("oi.unit_price_inr")
            * col("oi.quantity")
        )
        .alias("gross_amount_inr"),

        col("oi.line_total_inr")
        .alias("net_revenue_inr"),
    )
)


print(
    "Fact rows generated:",
    fact_sales.count()
)


# =========================================================
# Data Quality Check
# =========================================================

print("\n===== FACT DATA QUALITY =====")


print(
    "Null order_item_id:",
    fact_sales.filter(
        col("order_item_id").isNull()
    ).count()
)


print(
    "Null customer_id:",
    fact_sales.filter(
        col("customer_id").isNull()
    ).count()
)


print(
    "Null product_id:",
    fact_sales.filter(
        col("product_id").isNull()
    ).count()
)


print(
    "Online orders:",
    fact_sales.filter(
        col("channel") == "Online"
    ).count()
)


print(
    "Physical store orders:",
    fact_sales.filter(
        col("channel") == "Physical Store"
    ).count()
)


# =========================================================
# Revenue Check
# =========================================================

print("\n===== REVENUE CHECK =====")


fact_sales.select(
    "gross_amount_inr",
    "net_revenue_inr"
).summary(
    "count",
    "mean",
    "min",
    "max"
).show()


# =========================================================
# Write to MySQL
# =========================================================

print("\n===== LOADING FACT_SALES INTO MYSQL =====")


fact_sales.write \
    .mode("append") \
    .jdbc(
        url=JDBC_URL,
        table="fact_sales",
        properties=JDBC_PROPERTIES
    )


print("\n" + "=" * 70)
print("FACT_SALES LOAD COMPLETED")
print("=" * 70)


spark.stop()