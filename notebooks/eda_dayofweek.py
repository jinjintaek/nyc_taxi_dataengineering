import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname="nyc_taxi",
    user="nyc_user",
    password="nyc_pass",
    host="localhost",
    port=5432
)

query = """
SELECT 
    EXTRACT(DOW FROM tpep_pickup_datetime) AS day_of_week,
    AVG(total_amount) AS avg_total
FROM taxi_data
GROUP BY day_of_week
ORDER BY day_of_week
"""

df = pd.read_sql(query, conn)
conn.close()

day_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
df['day_of_week'] = df['day_of_week'].astype(int)
df['day_label'] = df['day_of_week'].apply(lambda x: day_labels[x])

plt.figure(figsize=(8, 5))
plt.bar(df['day_label'], df['avg_total'])
plt.title('Average Total Amount by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Average Total Amount ($)')
plt.tight_layout()
plt.show()