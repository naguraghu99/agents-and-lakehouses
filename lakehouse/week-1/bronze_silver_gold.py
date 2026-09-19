"""
Week 1 — Day 1: Bronze / Silver / Gold Medallion Architecture
==============================================================
Run this inside the Spark container (Docker) to:
  1. Generate raw simulated trade data
  2. Land it in the BRONZE layer (raw, unmodified)
  3. Clean, dedupe, and validate into the SILVER layer
  4. Build business aggregates in the GOLD layer

Prerequisite: `podman-compose up -d` (RustFS running on localhost:9000)
"""

import os
import sys
import glob

# Ensure PySpark is importable when running inside the jupyter/pyspark-notebook image,
# where PYTHONPATH is not pre-set with Spark's bundled Python libraries.
for spark_dir in ("/usr/local/spark", "/opt/spark"):
    if os.path.isdir(spark_dir):
        pyspark_python = os.path.join(spark_dir, "python")
        if os.path.isdir(pyspark_python) and pyspark_python not in sys.path:
            sys.path.insert(0, pyspark_python)
        py4j_zip = glob.glob(os.path.join(pyspark_python, "lib", "py4j-*.zip"))
        if py4j_zip and py4j_zip[0] not in sys.path:
            sys.path.insert(0, py4j_zip[0])

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import (
    StructType, StructField,
    StringType, DoubleType, LongType, TimestampType
)

# ------------------------------------------------------------------
# 1. Spark session with RustFS (S3) + Hadoop AWS support
# ------------------------------------------------------------------
def create_spark():
    return (
        SparkSession.builder
        .appName("bronze-silver-gold")
        .config("spark.hadoop.fs.s3a.endpoint", "http://rustfs:9000")
        .config("spark.hadoop.fs.s3a.access.key", "admin")
        .config("spark.hadoop.fs.s3a.secret.key", "password")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .getOrCreate()
    )


# ------------------------------------------------------------------
# 2. Simulate raw trade data (as if streaming in from Kafka/NiFi)
# ------------------------------------------------------------------
TRADE_SCHEMA = StructType([
    StructField("trade_id", StringType()),
    StructField("symbol", StringType()),
    StructField("price", DoubleType()),
    StructField("quantity", LongType()),
    StructField("side", StringType()),         # BUY / SELL
    StructField("event_time", TimestampType()),
    StructField("raw_payload", StringType())   # keep raw JSON-ish string
])

def generate_raw_trades(spark, num_rows=100):
    # Synthesize a small, realistic dataset inline.
    rows = []
    import random
    import datetime as dt

    symbols = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA"]
    sides = ["BUY", "SELL"]

    for i in range(num_rows):
        ts = dt.datetime(2025, 1, 6) + dt.timedelta(minutes=i)
        # Inject some duplicated trade_ids to test dedup in Silver.
        tid = f"TRADE-{i % 90:05d}"
        rows.append((
            tid,
            random.choice(symbols),
            round(random.uniform(100, 900), 2),
            random.randint(1, 100),
            random.choice(sides),
            ts,
            f'{{"trade_id":"{tid}","source":"sim"}}'
        ))
    return spark.createDataFrame(rows, TRADE_SCHEMA)


# ------------------------------------------------------------------
# 3. Write to BRONZE (raw, append-only, partition by event date)
# ------------------------------------------------------------------
def write_bronze(df):
    bronze_path = "s3a://bronze/trades"
    df = df.withColumn("event_date", F.date_format(F.col("event_time"), "yyyyMMdd"))
    df.write.mode("append") \
      .partitionBy("event_date") \
      .parquet(bronze_path)
    print(f"[BRONZE] {df.count()} rows written to {bronze_path}")
    return bronze_path


# ------------------------------------------------------------------
# 4. Read BRONZE, clean + dedupe into SILVER
# ------------------------------------------------------------------
def build_silver(spark, bronze_path):
    df = spark.read.parquet(bronze_path)

    silver = (
        df
        # Drop the raw payload — we don't need it downstream.
        .drop("raw_payload")
        # Basic validation: only valid rows move forward.
        .filter(
            (F.col("price") > 0)
            & (F.col("quantity") > 0)
            & F.col("trade_id").isNotNull()
        )
        # Deduplicate on business key, keeping the latest event.
        .withColumn("rn", F.row_number().over(
            Window.partitionBy("trade_id").orderBy(F.col("event_time").desc())
        ))
        .filter(F.col("rn") == 1)
        .drop("rn")
    )

    return silver


# ------------------------------------------------------------------
# 5. Build GOLD aggregates (e.g., daily symbol summary)
# ------------------------------------------------------------------
def build_gold(spark, silver):
    gold = (
        silver
        .groupBy(
            F.date_format(F.col("event_time"), "yyyyMMdd").alias("trade_date"),
            F.col("symbol")
        )
        .agg(
            F.count("*").alias("num_trades"),
            F.sum(F.when(F.col("side") == "BUY", F.col("quantity")).otherwise(0)).alias("buy_quantity"),
            F.sum(F.when(F.col("side") == "SELL", F.col("quantity")).otherwise(0)).alias("sell_quantity"),
            F.avg("price").alias("avg_price"),
            F.min("price").alias("min_price"),
            F.max("price").alias("max_price")
        )
        .orderBy("trade_date", "symbol")
    )
    return gold


# ------------------------------------------------------------------
# 6. Main
# ------------------------------------------------------------------
def main():
    spark = create_spark()
    print("Spark session created.")

    raw = generate_raw_trades(spark, num_rows=100)
    raw.show(5, truncate=False)

    bronze_path = write_bronze(raw)

    silver = build_silver(spark, bronze_path)
    print(f"[SILVER] {silver.count()} clean rows")
    silver.write.mode("overwrite").parquet("s3a://silver/trades")
    silver.show(5)

    gold = build_gold(spark, silver)
    gold.write.mode("overwrite").parquet("s3a://gold/daily_symbol_summary")
    gold.show(10)

    print("\n✅ Medallion pipeline complete.")
    print("  Bronze: s3a://bronze/trades")
    print("  Silver: s3a://silver/trades")
    print("  Gold:   s3a://gold/daily_symbol_summary")


if __name__ == "__main__":
    main()