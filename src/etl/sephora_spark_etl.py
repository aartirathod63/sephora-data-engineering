from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum as spark_sum,
    round as spark_round,
    when,
    lit,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
)


# =========================================================
# Spark Session
# =========================================================

spark = (
    SparkSession.builder
    .appName("SephoraIndiaETL")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


print("=" * 70)
print("SEPHORA INDIA DATA ENGINEERING PIPELINE")
print("=" * 70)

print(f"Spark Version: {spark.version}")


# =========================================================
# Paths
# =========================================================

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"


# =========================================================
# Schemas
# =========================================================

product_schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_name", StringType(), True),
    StructField("brand", StringType(), True),
    StructField("category", StringType(), True),
    StructField("subcategory", StringType(), True),
    StructField("mrp_inr", IntegerType(), True),
    StructField("rating", DoubleType(), True),
    StructField("review_count", IntegerType(), True),
    StructField("size", StringType(), True),
    StructField("stock_quantity", IntegerType(), True),
])


customer_schema = StructType([
    StructField("customer_id", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("gender", StringType(), True),
    StructField("signup_date", StringType(), True),
    StructField("loyalty_tier", StringType(), True),
])


store_schema = StructType([
    StructField("store_id", StringType(), True),
    StructField("store_name", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("mall", StringType(), True),
    StructField("area", StringType(), True),
    StructField("store_type", StringType(), True),
])


order_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("store_id", StringType(), True),
    StructField("order_date", StringType(), True),
    StructField("channel", StringType(), True),
    StructField("payment_method", StringType(), True),
    StructField("order_status", StringType(), True),
])


order_item_schema = StructType([
    StructField("order_item_id", StringType(), True),
    StructField("order_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price_inr", DoubleType(), True),
    StructField("discount_percent", IntegerType(), True),
    StructField("discount_amount_inr", DoubleType(), True),
    StructField("line_total_inr", DoubleType(), True),
])


# =========================================================
# Read Raw Data
# =========================================================

print("\n===== READING RAW DATA =====")

products = (
    spark.read
    .schema(product_schema)
    .option("header", True)
    .csv(f"{RAW_PATH}/products.csv")
)

customers = (
    spark.read
    .schema(customer_schema)
    .option("header", True)
    .csv(f"{RAW_PATH}/customers.csv")
)

stores = (
    spark.read
    .schema(store_schema)
    .option("header", True)
    .csv(f"{RAW_PATH}/stores.csv")
)

orders = (
    spark.read
    .schema(order_schema)
    .option("header", True)
    .csv(f"{RAW_PATH}/orders.csv")
)

order_items = (
    spark.read
    .schema(order_item_schema)
    .option("header", True)
    .csv(f"{RAW_PATH}/order_items.csv")
)


# =========================================================
# Row Counts
# =========================================================

print("\n===== RAW ROW COUNTS =====")

print("Products:", products.count())
print("Customers:", customers.count())
print("Stores:", stores.count())
print("Orders:", orders.count())
print("Order Items:", order_items.count())


# =========================================================
# Data Quality Checks
# =========================================================

print("\n===== DATA QUALITY CHECKS =====")


def check_nulls(df, table_name):

    null_condition = None

    for column_name in df.columns:

        condition = col(column_name).isNull()

        if null_condition is None:
            null_condition = condition
        else:
            null_condition = (
                null_condition | condition
            )

    null_count = (
        df.filter(null_condition)
        .count()
    )

    print(
        f"{table_name} null rows: {null_count}"
    )


check_nulls(
    products,
    "Products"
)

check_nulls(
    customers,
    "Customers"
)

check_nulls(
    stores,
    "Stores"
)

check_nulls(
    orders,
    "Orders"
)

check_nulls(
    order_items,
    "Order Items"
)


# =========================================================
# Duplicate Checks
# =========================================================

print("\n===== DUPLICATE CHECKS =====")


def check_duplicates(
    df,
    key_column,
    table_name
):

    duplicate_count = (
        df.groupBy(key_column)
        .count()
        .filter(col("count") > 1)
        .count()
    )

    print(
        f"{table_name} duplicate {key_column}: "
        f"{duplicate_count}"
    )


check_duplicates(
    products,
    "product_id",
    "Products"
)

check_duplicates(
    customers,
    "customer_id",
    "Customers"
)

check_duplicates(
    stores,
    "store_id",
    "Stores"
)

check_duplicates(
    orders,
    "order_id",
    "Orders"
)

check_duplicates(
    order_items,
    "order_item_id",
    "Order Items"
)


# =========================================================
# Referential Integrity
# =========================================================

print("\n===== REFERENTIAL INTEGRITY =====")


invalid_customer_orders = (
    orders
    .join(
        customers.select("customer_id"),
        on="customer_id",
        how="left_anti"
    )
)

print(
    "Orders with invalid customer_id:",
    invalid_customer_orders.count()
)


invalid_order_items = (
    order_items
    .join(
        orders.select("order_id"),
        on="order_id",
        how="left_anti"
    )
)

print(
    "Order items with invalid order_id:",
    invalid_order_items.count()
)


invalid_products = (
    order_items
    .join(
        products.select("product_id"),
        on="product_id",
        how="left_anti"
    )
)

print(
    "Order items with invalid product_id:",
    invalid_products.count()
)


# =========================================================
# Business Validation
# =========================================================

print("\n===== BUSINESS VALIDATION =====")


invalid_quantity = (
    order_items
    .filter(col("quantity") <= 0)
    .count()
)

print(
    "Invalid quantities:",
    invalid_quantity
)


invalid_prices = (
    order_items
    .filter(col("unit_price_inr") <= 0)
    .count()
)

print(
    "Invalid unit prices:",
    invalid_prices
)


invalid_discount = (
    order_items
    .filter(
        (col("discount_percent") < 0)
        |
        (col("discount_percent") > 100)
    )
    .count()
)

print(
    "Invalid discounts:",
    invalid_discount
)


# =========================================================
# Revenue Transformation
# =========================================================

print("\n===== REVENUE TRANSFORMATION =====")


order_items_clean = (
    order_items
    .withColumn(
        "gross_amount_inr",
        col("unit_price_inr")
        * col("quantity")
    )
    .withColumn(
        "net_revenue_inr",
        spark_round(
            col("gross_amount_inr")
            - col("discount_amount_inr"),
            2
        )
    )
)


# =========================================================
# Join Transaction Data
# =========================================================

print("\n===== BUILDING ANALYTICAL DATASET =====")


sales = (
    order_items_clean.alias("oi")

    .join(
        orders.alias("o"),
        col("oi.order_id")
        == col("o.order_id"),
        "inner"
    )

    .join(
        products.alias("p"),
        col("oi.product_id")
        == col("p.product_id"),
        "inner"
    )

    .join(
        customers.alias("c"),
        col("o.customer_id")
        == col("c.customer_id"),
        "inner"
    )

    .join(
        stores.alias("s"),
        col("o.store_id")
        == col("s.store_id"),
        "left"
    )

    .select(
        col("oi.order_item_id"),
        col("o.order_id"),
        col("o.order_date"),
        col("o.customer_id"),
        col("c.city").alias("customer_city"),
        col("c.loyalty_tier"),
        col("o.store_id"),
        col("s.store_name"),
        col("o.channel"),
        col("o.payment_method"),
        col("o.order_status"),
        col("oi.product_id"),
        col("p.product_name"),
        col("p.brand"),
        col("p.category"),
        col("p.subcategory"),
        col("oi.quantity"),
        col("oi.unit_price_inr"),
        col("oi.discount_percent"),
        col("oi.discount_amount_inr"),
        col("oi.net_revenue_inr"),
    )
)


print(
    "Analytical dataset rows:",
    sales.count()
)


# =========================================================
# Revenue by Category
# =========================================================

print("\n===== REVENUE BY CATEGORY =====")

revenue_by_category = (
    sales
    .groupBy("category")
    .agg(
        spark_round(
            spark_sum("net_revenue_inr"),
            2
        ).alias("total_revenue_inr")
    )
    .orderBy(
        col("total_revenue_inr").desc()
    )
)

revenue_by_category.show(
    truncate=False
)


# =========================================================
# Revenue by Channel
# =========================================================

print("\n===== REVENUE BY CHANNEL =====")

revenue_by_channel = (
    sales
    .groupBy("channel")
    .agg(
        spark_round(
            spark_sum("net_revenue_inr"),
            2
        ).alias("total_revenue_inr")
    )
    .orderBy(
        col("total_revenue_inr").desc()
    )
)

revenue_by_channel.show(
    truncate=False
)


# =========================================================
# Revenue by Loyalty Tier
# =========================================================

print("\n===== REVENUE BY LOYALTY TIER =====")

revenue_by_loyalty = (
    sales
    .groupBy("loyalty_tier")
    .agg(
        spark_round(
            spark_sum("net_revenue_inr"),
            2
        ).alias("total_revenue_inr")
    )
    .orderBy(
        col("total_revenue_inr").desc()
    )
)

revenue_by_loyalty.show(
    truncate=False
)


# =========================================================
# Write Processed Data
# =========================================================

print("\n===== WRITING PROCESSED DATA =====")

(
    sales
    .write
    .mode("overwrite")
    .partitionBy("channel")
    .parquet(
        f"{PROCESSED_PATH}/sales"
    )
)


(
    revenue_by_category
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(
        f"{PROCESSED_PATH}/revenue_by_category"
    )
)


(
    revenue_by_channel
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(
        f"{PROCESSED_PATH}/revenue_by_channel"
    )
)


print("\n===== ETL COMPLETED SUCCESSFULLY =====")


# =========================================================
# Stop Spark
# =========================================================

spark.stop()