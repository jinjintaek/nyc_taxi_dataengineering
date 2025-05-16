import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

conn = psycopg2.connect(
    dbname="nyc_taxi",
    user="nyc_user",
    password="nyc_pass",
    host="localhost",
    port=5432
)

# 1. 시간대별 평균 요금
query1 = """
SELECT 
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
    AVG(total_amount) AS avg_total
FROM taxi_data
GROUP BY hour
ORDER BY hour
"""
df1 = pd.read_sql(query1, conn)

plt.figure(figsize=(8,5))
plt.plot(df1['hour'], df1['avg_total'], marker='o')
plt.title('Average Total Amount by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Average Total Amount ($)')
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. 승객 수별 평균 요금
query2 = """
SELECT 
    passenger_count,
    AVG(total_amount) AS avg_total
FROM taxi_data
GROUP BY passenger_count
ORDER BY passenger_count
"""
df2 = pd.read_sql(query2, conn)

plt.figure(figsize=(8,5))
plt.bar(df2['passenger_count'], df2['avg_total'])
plt.title('Average Total Amount by Passenger Count')
plt.xlabel('Passenger Count')
plt.ylabel('Average Total Amount ($)')
plt.tight_layout()
plt.show()

# 3. 거리별 총 요금 분포
query3 = """
SELECT trip_distance, total_amount FROM taxi_data
WHERE trip_distance < 50 AND total_amount < 200
LIMIT 10000
"""
df3 = pd.read_sql(query3, conn)
conn.close()

plt.figure(figsize=(8,5))
sns.scatterplot(data=df3, x='trip_distance', y='total_amount', alpha=0.2)
plt.title('Total Amount vs. Trip Distance')
plt.xlabel('Trip Distance (miles)')
plt.ylabel('Total Amount ($)')
plt.tight_layout()
plt.show()