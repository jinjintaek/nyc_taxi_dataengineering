import os
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

for filename in os.listdir(RAW_DIR):
    if filename.endswith(".parquet"):
        file_path = os.path.join(RAW_DIR, filename)
        print(f"[PROCESSING] {filename}")

        # Load data
        df = pd.read_parquet(file_path)

        # Convert datetime columns
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], errors='coerce')
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], errors='coerce')

        # Filter invalid rows
        df = df[df['trip_distance'] > 0]
        df = df[df['fare_amount'] >= 0]

        # Drop missing values
        df = df.dropna()

        # Save to CSV
        output_filename = filename.replace(".parquet", ".csv")
        output_path = os.path.join(PROCESSED_DIR, output_filename)
        df.to_csv(output_path, index=False)

        print(f"[SAVED] Cleaned data to {output_path}")