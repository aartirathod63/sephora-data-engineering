from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    when,
    to_date,
    year,
    quarter,
    month,
    date_format,
    dayofmonth,
    weekofyear,
)

# =========================================================
# Spark Session
# =========================================================

spark = (
    SparkSession.builder
    .appName("SephoraMySQLLoader")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


print("=" * 70)
print("SEPHORA MYSQL DATA WAREHOUSE LOADER")
print("=" * 70)

print(f"Spark Version: {spark.version}")


# =========================================================
# MySQL Configuration
# =========================================================

MYSQL_HOST = "localhost"

MYSQL_PORT = "3306"

MYSQL_DATABASE = "sephora_analytics"

MYSQL_USER = "root"

MYSQL_PASSWORD = "Aarti@123code src/etl/load_to_mysql.py"


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
# Raw Data Paths
# =========================================================

RAW_PATH = "data/raw"


# =========================================================
# Read Data
# =========================================================

print("\n===== READING SOURCE DATA =====")


customers = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{RAW_PATH}/customers.csv")
)


products = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{RAW_PATH}/products.csv")
)


stores = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{RAW_PATH}/stores.csv")
)


orders = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{RAW_PATH}/orders.csv")
)


order_items = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{RAW_PATH}/order_items.csv")
)


# =========================================================
# CUSTOMER DIMENSION
# =========================================================

print("\n===== LOADING DIM_CUSTOMER =====")


dim_customer = (
    customers
    .select(
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "city",
        "state",
        "age",
        "gender",
        "signup_date",
        "loyalty_tier",
    )
    .withColumn(
        "signup_date",
        to_date(col("signup_date"))
    )
)


print(
    "dim_customer rows:",
    dim_customer.count()
)


dim_customer.write \
    .mode("append") \
    .jdbc(
        url=JDBC_URL,
        table="dim_customer",
        properties=JDBC_PROPERTIES
    )


# =========================================================
# PRODUCT DIMENSION
# =========================================================

print("\n===== LOADING DIM_PRODUCT =====")


dim_product = (
    products
    .select(
        "product_id",
        "product_name",
        "brand",
        "category",
        "subcategory",
        "mrp_inr",
        "rating",
        "review_count",
        "size",
        "stock_quantity",
    )
)


print(
    "dim_product rows:",
    dim_product.count()
)


dim_product.write \
    .mode("append") \
    .jdbc(
        url=JDBC_URL,
        table="dim_product",
        properties=JDBC_PROPERTIES
    )


# =========================================================
# STORE DIMENSION
# =========================================================

print("\n===== LOADING DIM_STORE =====")


dim_store = (
    stores
    .select(
        "store_id",
        "store_name",
        "city",
        "state",
        "mall",
        "area",
        "store_type",
    )
)


print(
    "dim_store rows:",
    dim_store.count()
)


dim_store.write \
    .mode("append") \
    .jdbc(
        url=JDBC_URL,
        table="dim_store",
        properties=JDBC_PROPERTIES
    )


# =========================================================
# DATE DIMENSION
# =========================================================

print("\n===== BUILDING DIM_DATE =====")


dates = (
    orders
    .select(
        to_date(
            col("order_date")
        ).alias("full_date")
    )
    .filter(
        col("full_date").isNotNull()
    )
    .distinct()
)


dim_date = (
    dates
    .withColumn(
        "date_id",
        date_format(
            col("full_date"),
            "yyyyMMdd"
        ).cast("int")
    )
    .withColumn(
        "year",
        year("full_date")
    )
    .withColumn(
        "quarter",
        quarter("full_date")
    )
    .withColumn(
        "month",
        month("full_date")
    )
    .withColumn(
        "month_name",
        date_format(
            "full_date",
            "MMMM"
        )
    )
    .withColumn(
        "day",
        dayofmonth("full_date")
    )
    .withColumn(
        "day_name",
        date_format(
            "full_date",
            "EEEE"
        )
    )
    .withColumn(
        "week",
        weekofyear("full_date")
    )
    .select(
        "date_id",
        "full_date",
        "year",
        "quarter",
        "month",
        "month_name",
        "day",
        "day_name",
        "week",
    )
)


print(
    "dim_date rows:",
    dim_date.count()
)


dim_date.write \
    .mode("append") \
    .jdbc(
        url=JDBC_URL,
        table="dim_date",
        properties=JDBC_PROPERTIES
    )


# =========================================================
# FACT SALES
# =========================================================

# =========================================================
# FACT SALES
# =========================================================

print("\n===== BUILDING FACT_SALES =====")


fact_sales = (
    order_items.alias("oi")

    .join(
        orders.alias("o"),
        col("oi.order_id") == col("o.order_id"),
        "inner"
    )

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

        col("warehouse_store_id").alias("store_id"),

        date_format(
            to_date(col("o.order_date")),
            "yyyyMMdd"
        ).cast("int").alias("date_id"),

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
        ).alias("gross_amount_inr"),

        col("oi.line_total_inr")
        .alias("net_revenue_inr"),
    )
)


print(
    "fact_sales rows:",
    fact_sales.count()
)


fact_sales.write \
    .mode("append") \
    .jdbc(
        url=JDBC_URL,
        table="fact_sales",
        properties=JDBC_PROPERTIES
    )

# =========================================================
# Finished
# =========================================================

print("\n" + "=" * 70)

print(
    "MYSQL DATA WAREHOUSE LOAD COMPLETED"
)

print("=" * 70)


spark.stop()
