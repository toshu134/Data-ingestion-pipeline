import time
from data_generation import generate_fake_data
from spark import (
    init_spark_session,
    write_to_delta,
    read_latest_data,
    get_current_version
)
from email_utils import send_email_summary

DATA_PATH = "delta_table"
INTERVAL_MINUTES = 5
ROWS_PER_BATCH = 1000
TIMEZONE = "Asia/Kolkata"

def run_pipeline():
    # 1. Start Spark session
    spark = init_spark_session(TIMEZONE)

    # 2. Generate fake data
    df_fake = generate_fake_data(num_records=ROWS_PER_BATCH)

    # 3. Convert to Spark DataFrame
    df_spark = spark.createDataFrame(df_fake)

    # 4. Get version before write
    version_before = get_current_version(DATA_PATH, spark)

    # 5. Write to Delta
    write_to_delta(df_spark, DATA_PATH)

    # 6. Get version after write
    version_after = get_current_version(DATA_PATH, spark)

    # 7. Read only newly added data (latest version)
    df_latest = read_latest_data(DATA_PATH, version_after, spark)

    # 8. Send email summary
    send_email_summary(df_latest, version_after)

    print(f"Batch written. Version changed from {version_before} → {version_after}.")

if __name__ == "__main__":
    while True:
        run_pipeline()
        time.sleep(INTERVAL_MINUTES * 60)
