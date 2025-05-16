import os
import psycopg2
import pandas as pd

PROCESSED_DIR = "data/processed"

conn = psycopg2.connect(
    dbname="nyc_taxi",
    user="nyc_user",
    password="nyc_pass",
    host="localhost",
    port=5432
)

cursor = conn.cursor()

for filename in os.listdir(PROCESSED_DIR):
    if filename.endswith(".csv"):
        file_path = os.path.join(PROCESSED_DIR, filename)
        print(f"[LOADING] {filename}")

        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.lower()
        df.rename(columns={'vendorid': 'vendor_id'}, inplace=True)
        print(f"[COLUMNS] {df.columns.tolist()}")

        required_columns = ['vendor_id', 'tpep_pickup_datetime', 'tpep_dropoff_datetime',
                            'passenger_count', 'trip_distance', 'fare_amount', 'total_amount']

        if not all(col in df.columns for col in required_columns):
            print(f"[SKIP] {filename} is missing required columns.")
            continue

        records = df[['vendor_id', 'tpep_pickup_datetime', 'tpep_dropoff_datetime',
                      'passenger_count', 'trip_distance', 'fare_amount', 'total_amount']].values.tolist()

        cursor.executemany("""
            INSERT INTO taxi_data (
                vendor_id, tpep_pickup_datetime, tpep_dropoff_datetime,
                passenger_count, trip_distance, fare_amount, total_amount
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, records)

        conn.commit()
        print(f"[DONE] Loaded {filename}")

cursor.close()
conn.close()
print("All files loaded successfully.")