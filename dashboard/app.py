

import streamlit as st
import pandas as pd
import psycopg2

st.title("NYC Taxi Dashboard")

# Sidebar filters
day_filter = st.sidebar.multiselect(
    "Select Day(s) of Week",
    options=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
)

hour_filter = st.sidebar.slider(
    "Hour of Pickup",
    min_value=0,
    max_value=23,
    value=(0, 23)
)

# Map day names to numbers
day_map = {
    "Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3,
    "Thursday": 4, "Friday": 5, "Saturday": 6
}
day_numbers = [day_map[d] for d in day_filter]

# SQL query with filters
query = f"""
SELECT
    EXTRACT(DOW FROM tpep_pickup_datetime) AS day_of_week,
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
    AVG(total_amount) AS avg_total
FROM taxi_data
WHERE
    EXTRACT(DOW FROM tpep_pickup_datetime) = ANY(%s)
    AND EXTRACT(HOUR FROM tpep_pickup_datetime) BETWEEN %s AND %s
GROUP BY day_of_week, hour
ORDER BY day_of_week, hour
"""

conn = psycopg2.connect(
    dbname="nyc_taxi",
    user="nyc_user",
    password="nyc_pass",
    host="localhost",
    port=5432
)

df = pd.read_sql(query, conn, params=(day_numbers, hour_filter[0], hour_filter[1]))
conn.close()

if df.empty:
    st.warning("No data found for the selected filters.")
else:
    # Mapping day numbers to names
    rev_day_map = {v: k for k, v in day_map.items()}
    df["day"] = df["day_of_week"].astype(int).map(rev_day_map)
    df["hour"] = df["hour"].astype(int)

    st.subheader("Average Total Amount by Day and Hour")

    # Line chart
    for day in sorted(df["day"].unique()):
        subset = df[df["day"] == day]
        st.line_chart(subset.set_index("hour")["avg_total"], height=300, use_container_width=True)