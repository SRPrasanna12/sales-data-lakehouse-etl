
import sqlite3
import pandas as pd
from pathlib import Path

# Project path
ROOT = Path(__file__).resolve().parents[1]

# Silver data
silver_file = ROOT / "data" / "silver" / "sales_silver.csv"

# Database path
database_file = ROOT / "sales.db"

# Read cleaned sales data
sales = pd.read_csv(silver_file)

# Connect to SQLite database
connection = sqlite3.connect(database_file)

try:
    # Load data into SQL table
    sales.to_sql(
        "sales",
        connection,
        if_exists="replace",
        index=False
    )

    print("Sales data loaded into SQLite successfully!")

    # SQL Query 1: Revenue by product
    query1 = """
    SELECT
        product,
        SUM(total_amount) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC;
    """

    result1 = pd.read_sql_query(query1, connection)

    print("\nRevenue by Product:")
    print(result1)

    # SQL Query 2: Total quantity sold
    query2 = """
    SELECT SUM(quantity) AS total_quantity
    FROM sales;
    """

    result2 = pd.read_sql_query(query2, connection)

    print("\nTotal Quantity Sold:")
    print(result2)

    # SQL Query 3: Total sales revenue
    query3 = """
    SELECT SUM(total_amount) AS total_revenue
    FROM sales;
    """

    result3 = pd.read_sql_query(query3, connection)

    print("\nTotal Sales Revenue:")
    print(result3)

    # SQL Query 4: Total number of orders
    query4 = """
    SELECT COUNT(DISTINCT order_id) AS total_orders
    FROM sales;
    """

    result4 = pd.read_sql_query(query4, connection)

    print("\nTotal Orders:")
    print(result4)

finally:
    connection.close()
