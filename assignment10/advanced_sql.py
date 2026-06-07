import sqlite3

conn = sqlite3.connect("../db/lesson.db")
cursor = conn.cursor()

conn.execute('PRAGMA foreign_keys = 1')

try:
#---------------Task1-------------------------------

    sql1 = """
    SELECT
        o.order_id,
        SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li
        ON o.order_id = li.order_id
    JOIN products p
        ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """

    cursor.execute(sql1)

    results = cursor.fetchall()

    for order_id, total_price in results:
        print(f"Order {order_id}: ${total_price:.2f}")

# ---------------Task 2----------------

    sql2 = """
    SELECT
        c.customer_name,
        AVG(order_totals.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT
            o.customer_id AS customer_id_b,
            SUM(p.price * li.quantity) AS total_price
        FROM orders o
        JOIN line_items li
            ON o.order_id = li.order_id
        JOIN products p
            ON li.product_id = p.product_id
        GROUP BY o.order_id, o.customer_id
    ) AS order_totals
    ON c.customer_id = order_totals.customer_id_b
    GROUP BY c.customer_id, c.customer_name
    ORDER BY c.customer_id;
    """

    print("\nAverage order value by customer:")
    cursor.execute(sql2)

    for customer_name, avg_price in cursor.fetchall():
        if avg_price is None:
            print(f"{customer_name}: No orders")
        else:
            print(f"{customer_name}: ${avg_price:.2f}")

    #--------------Task3--------------------------------------

    # --- Get customer_id ---
    cursor.execute("""
        SELECT customer_id
        FROM customers
        WHERE customer_name = ?
    """, ("Perez and Sons",))
    customer_id = cursor.fetchone()[0]

    # --- Get employee_id ---
    cursor.execute("""
        SELECT employee_id
        FROM employees
        WHERE first_name = ? AND last_name = ?
    """, ("Miranda", "Harris"))
    employee_id = cursor.fetchone()[0]

    # --- Get 5 cheapest products ---
    cursor.execute("""
        SELECT product_id
        FROM products
        ORDER BY price
        LIMIT 5
    """)
    product_ids = [row[0] for row in cursor.fetchall()]

    # --- TRANSACTION START ---
    conn.execute("BEGIN")

    # Create order
    cursor.execute("""
        INSERT INTO orders (customer_id, employee_id, date)
        VALUES (?, ?, CURRENT_DATE)
     """, (customer_id, employee_id))

    order_id = cursor.lastrowid

    # Insert line items
    for pid in product_ids:
        cursor.execute("""
            INSERT INTO line_items (order_id, product_id, quantity)
            VALUES (?, ?, ?)
        """, (order_id, pid, 10))

    conn.commit()

    # --- Verify output ---
    cursor.execute("""
        SELECT
            li.line_item_id,
            li.quantity,
            p.product_name
        FROM line_items li
        JOIN products p
            ON li.product_id = p.product_id
        WHERE li.order_id = ?
        ORDER BY li.line_item_id
    """, (order_id,))

    print(f"\nOrder {order_id} line items:")

    for line_item_id, qty, name in cursor.fetchall():
        print(line_item_id, qty, name)

    #--------------Task 4--------------------------------------------

    print("\nEmployees with more than 5 orders:")

    cursor.execute("""
        SELECT
            e.employee_id,
            e.first_name,
            e.last_name,
            COUNT(o.order_id) AS order_count
        FROM employees e
        JOIN orders o
            ON e.employee_id = o.employee_id
        GROUP BY
            e.employee_id,
            e.first_name,
            e.last_name
        HAVING COUNT(o.order_id) > 5
        ORDER BY e.employee_id;
    """)

    for emp_id, first, last, count in cursor.fetchall():
        print(emp_id, first, last, count)

except Exception as e:
    conn.rollback()
    print("Error:", e)

finally:
    conn.close()

