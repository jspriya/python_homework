import pandas as pd
import sqlite3

conn = None

try:
    # Connect to the lesson database
    conn = sqlite3.connect("../db/lesson.db")
    print("Connected to lesson.db successfully.\n")

    # Step 1: Read data into a DataFrame using a JOIN query
    query = """
    SELECT 
        line_items.line_item_id, 
        line_items.quantity, 
        products.product_id, 
        products.product_name, 
        products.price
    FROM line_items
    JOIN products ON line_items.product_id = products.product_id
    """
    df = pd.read_sql_query(query, conn)
    
    print("--- Step 1: First 5 lines of the initial DataFrame ---")
    print(df.head(5))
    print()

    # Step 2: Add a calculated 'total' column
    df['total'] = df['quantity'] * df['price']
    
    print("--- Step 2: First 5 lines with the 'total' column added ---")
    print(df.head(5))
    print()

    # Step 3: Group by product_id and aggregate the data
    # 'count': matches how many times it was ordered
    # 'sum': calculates total revenue per product
    # 'first': keeps the string name of the product
    summary_df = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    })

    # Rename column names to make the summary cleaner
    summary_df = summary_df.rename(columns={'line_item_id': 'order_count'})

    print("--- Step 3: First 5 lines of the Grouped/Aggregated DataFrame ---")
    print(summary_df.head(5))
    print()

    # Step 4: Sort the DataFrame by the product_name column
    summary_df = summary_df.sort_values(by='product_name', ascending=True)
    
    print("--- Step 4: Sorted by Product Name ---")
    print(summary_df)
    print()

    # Step 5: Write the DataFrame to a CSV file in the working directory
    summary_df.to_csv("order_summary.csv", index=True)
    print("Success: order_summary.csv has been written to the assignment9 directory.")

except Exception as e:
    print("An error occurred:", e)

finally:
    if conn:
        conn.close()
        print("Database connection closed.")
