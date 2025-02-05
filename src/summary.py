import os
import dotenv
import psycopg2
import pandas as pd
from tabulate import tabulate

dotenv.load_dotenv()
dotenv.load_dotenv('../.env-kafka', override=True)
dotenv.load_dotenv('../.env-pg', override=True)
dotenv.load_dotenv('../.env-opensearch', override=True)

def get_db_connection():
    print(f"Connecting to {os.environ.get('AIVEN_PG_HOST')}")
    conn = psycopg2.connect(
        host=os.environ.get('AIVEN_PG_HOST'),
        port=os.environ.get('AIVEN_PG_PORT'),
        dbname=os.environ.get('AIVEN_PG_DB_NAME'),
        user=os.environ.get('AIVEN_PG_USER'),
        password=os.environ.get('AIVEN_PG_PASSWORD')
    )
    return conn

def fetch_hourly_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    with open('../sql/clickstream_hourly_stats.sql', 'r') as file:
        query = file.read()

    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return pd.DataFrame(rows, columns=columns)

def fetch_session_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    with open('../sql/clickstream_session_stats.sql', 'r') as file:
        query = file.read()

    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return pd.DataFrame(rows, columns=columns)

def display_stats(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    df = fetch_hourly_stats()
    display_stats(df)

    df = fetch_session_stats()
    display_stats(df)