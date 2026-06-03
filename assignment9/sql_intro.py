
import sqlite3

conn = None

try:
    conn = sqlite3.connect("../db/magazines.db")
    print("Connected to database.")

    # Task 3 Requirement: Enable foreign keys immediately
    conn.execute("PRAGMA foreign_keys = 1")

    cursor = conn.cursor()

    # Task 2: Define Structure safely using IF NOT EXISTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publishers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS magazines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        publisher_id INTEGER NOT NULL,
        FOREIGN KEY (publisher_id) REFERENCES publishers(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        subscriber_id INTEGER NOT NULL,
        magazine_id INTEGER NOT NULL,
        expiration_date TEXT NOT NULL,
        PRIMARY KEY (subscriber_id, magazine_id),
        FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
        FOREIGN KEY (magazine_id) REFERENCES magazines(id)
    )
    """)
    # Task 3: Helper functions returning IDs to prevent duplication breaking FKs

    def add_publisher(conn, name):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM publishers WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        if row is None:
            cursor.execute("INSERT INTO publishers(name) VALUES (?)", (name,))
            return cursor.lastrowid
        return row[0]

    def add_magazine(conn, name, publisher_id):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        if row is None:
            cursor.execute("INSERT INTO magazines(name, publisher_id) VALUES (?, ?)", (name, publisher_id))
            return cursor.lastrowid
        return row[0]

    def add_subscriber(conn, name, address):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (name, address))
        row = cursor.fetchone()
        
        if row is None:
            cursor.execute("INSERT INTO subscribers(name, address) VALUES (?, ?)", (name, address))
            return cursor.lastrowid
        return row[0]

    def add_subscription(conn, subscriber_id, magazine_id, expiration_date):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM subscriptions 
            WHERE subscriber_id = ? AND magazine_id = ?
        """, (subscriber_id, magazine_id))
        
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) 
                VALUES (?, ?, ?)
            """, (subscriber_id, magazine_id, expiration_date))

    # Populate Data safely using the dynamic returned IDs
    pub1_id = add_publisher(conn, "National Geographic")
    pub2_id = add_publisher(conn, "Time")
    pub3_id = add_publisher(conn, "Vogue")

    mag1_id = add_magazine(conn, "NatGeo Kids", pub1_id)
    mag2_id = add_magazine(conn, "Time Weekly", pub2_id)
    mag3_id = add_magazine(conn, "Vogue US", pub3_id)

    sub1_id = add_subscriber(conn, "Alice Johnson", "123 Main St")
    sub2_id = add_subscriber(conn, "Bob Smith", "456 Oak Ave")
    sub3_id = add_subscriber(conn, "Charlie Brown", "789 Pine Rd") 

    add_subscription(conn, sub1_id, mag1_id, "2027-01-01")
    add_subscription(conn, sub1_id, mag2_id, "2027-06-01")
    add_subscription(conn, sub2_id, mag3_id, "2026-12-31")

    # Write SQL Queries

    print("--- Query 1: All Subscribers ---")
    cursor.execute("SELECT * FROM subscribers")
    subscribers = cursor.fetchall()
    for sub in subscribers:
        print(sub)
    print()

    print("--- Query 2: Magazines Sorted by Name ---")
    cursor.execute("SELECT * FROM magazines ORDER BY name ASC")
    magazines = cursor.fetchall()
    for mag in magazines:
        print(mag)
    print()

    print("--- Query 3: Magazines for National Geographic (JOIN) ---")
    # This query uses an INNER JOIN to connect the two tables via the foreign key
    cursor.execute("""
        SELECT magazines.id, magazines.name, publishers.name 
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.id
        WHERE publishers.name = ?
    """, ("National Geographic",))
    joined_results = cursor.fetchall()
    for row in joined_results:
        print(row)
    print()

    conn.commit()
    print("Database populated and committed successfully.")

except sqlite3.Error as e:
    print("Database error:", e)

finally:
    if conn:
        conn.close()
        print("Connection closed.")


