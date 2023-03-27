import psycopg2

# Establish a connection to the database
conn = psycopg2.connect(
    host='124.123.26.241',
    port='5435',
    database='merck',
    user='postgres',
    password='iCtnMBWbLvHhsoUB7eFgZmUKblD1Mudv'
)


def query_database(serielnumber):
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    cur.execute(f"SELECT action_status FROM device where serial_number='{serielnumber}'")

    # Fetch all the results of the query
    results = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Return the results
    return results
