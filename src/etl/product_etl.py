from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def create_spark_session():
    return (
        SparkSession.builder
        .appName("SephoraProductETL")
        .master("local[*]")
        .getOrCreate()
    )


def main():
    spark = create_spark_session()

    print("Spark Version:", spark.version)

    # Read raw product data
    products = spark.read.csv(
        "data/raw/products.csv",
        header=True,
        inferSchema=True
    )

    print("\n===== RAW DATA =====")
    products.show()

    print("\n===== SCHEMA =====")
    products.printSchema()

    # Basic data-quality filtering
    products_clean = products.filter(
        (col("mrp_inr") > 0) &
        (col("rating").between(0, 5)) &
        (col("stock_quantity") >= 0)
    )

    print("\n===== CLEAN DATA =====")
    products_clean.show()

    print("\nTotal products:", products_clean.count())

    spark.stop()


if __name__ == "__main__":
    main()