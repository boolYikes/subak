from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, count, desc

spark = SparkSession.builder \
        .appName("Agg, join test") \
        .getOrCreate()

# Load
users = spark.read.parquet("parquet_data/users.parquet")
txns = spark.read.parquet("parquet_data/transactions.parquet")

# is this lazy?
joined = txns.join(users, on="user_id", how="inner")

agg1 = joined.groupBy("region", "product_category") \
    .agg(
        _sum("amount").alias("total_spent"),
        avg("amount").alias("avg_spent"),
        count("*").alias("num_txns")
    ) \
    .orderBy(desc("total_spent"))

agg1.show(20, truncate=False)

# 2
top_spenders = joined.groupBy("user_id", "name") \
    .agg(_sum("amount").alias("total_spent")) \
    .orderBy(desc("total_spent")) \
    .limit(10)

top_spenders.show(truncate=False)

spark.stop()