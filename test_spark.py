from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SephoraAnalytics")
    .master("local[*]")
    .getOrCreate()
)

print("=================================")
print("Spark is working!")
print("Spark version:", spark.version)
print("=================================")

data = [
    (1, "Lipstick", 25.0),
    (2, "Foundation", 40.0),
    (3, "Mascara", 30.0),
]

df = spark.createDataFrame(
    data,
    ["product_id", "product_name", "price"]
)

df.show()

spark.stop()