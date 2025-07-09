from pyspark.sql import SparkSession
from delta.tables import DeltaTable
import pytz
from datetime import datetime

def init_spark_session(timezone):
    return SparkSession.builder \
        .appName("DeltaIngestionPipeline") \
        .config("spark.sql.session.timeZone", timezone) \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

        
def write_to_delta(df_spark, path):
    df_spark.write.format("delta").mode("append").save(path)
    
def get_current_version(path, spark):
    try:
        delta_table = DeltaTable.forPath(spark, path)
        history_df = delta_table.history()
        return history_df.select("version").head()[0]
    except:
        return -1

def read_latest_data(path, version, spark):
    return spark.read.format("delta").option("versionAsOf", version).load(path)