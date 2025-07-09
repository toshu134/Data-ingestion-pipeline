from faker import Faker
import pandas as pd
from datetime import datetime
import os

fake = Faker()
CSV_FILE = "incoming_data.csv"

def generate_fake_data(num_records):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [{
        "name": fake.name(),
        "address": fake.address().replace("\n", ", "),
        "email": fake.email(),
        "ingested_at": current_time
    } for _ in range(num_records)]
    return pd.DataFrame(data)

def append_to_csv(df, filename):
    file_exists = os.path.isfile(filename)
    df.to_csv(filename, mode='a', header=not file_exists, index=False)

if __name__ == "__main__":
    df = generate_fake_data(100)
    append_to_csv(df, CSV_FILE)
    print(df.info())
