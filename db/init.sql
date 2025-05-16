CREATE TABLE IF NOT EXISTS taxi_data (
    vendor_id INTEGER,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    trip_distance FLOAT,
    fare_amount FLOAT,
    total_amount FLOAT
);