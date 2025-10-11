import streamlit as st
import pandas as pd
import sqlite3

# Page configuration
st.set_page_config(page_title="Revenue Dashboard", layout="wide")
st.title("📊 Monthly Revenue Dashboard")

# Create database
conn = sqlite3.connect(':memory:')

# Generate 36 months of data (100 to 1000)
months = pd.date_range('2022-01-01', periods=36, freq='MS')
revenues = [100 + (900/35) * i for i in range(36)]

# Create dataframe
data = pd.DataFrame({
    'month': months,
    'revenue': revenues
})

# Load into database
data.to_sql('monthly_revenue', conn, index=False, if_exists='replace')

# SQL Query
query = """
SELECT 
    month,
    ROUND(revenue, 2) as revenue
FROM monthly_revenue
ORDER BY month
"""

# Execute query
df = pd.read_sql(query, conn)
df['month'] = pd.to_datetime(df['month'])

# Display bar chart
st.subheader("Revenue Growth Over 36 Months")
st.bar_chart(df.set_index('month')['revenue'])

# Show the data table
st.subheader("Data Table")
st.dataframe(df, use_container_width=True)

# Close connection
conn.close()