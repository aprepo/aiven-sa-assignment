import os
import dotenv
import psycopg2
from psycopg2.extras import execute_values

dotenv.load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('AIVEN_PG_HOST'),
        port=os.environ.get('AIVEN_PG_PORT'),
        dbname=os.environ.get('AIVEN_PG_DB_NAME'),
        user=os.environ.get('AIVEN_PG_USER'),
        password=os.environ.get('AIVEN_PG_PASSWORD')
    )
    return conn

def write_to_db(event):
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO clickstream_events (
        timestamp, 
        event_id, 
        user_id, 
        session_id, 
        event_type, 
        page_url, 
        referrer_url, 
        user_agent, 
        ip_address, 
        device
    ) VALUES %s
    """

    values = [
        (
            event['timestamp'],
            event.get('event_id'),
            event['user_id'],
            event['session_id'],
            event['event_type'],
            event['page_url'],
            event.get('referrer_url'),
            event.get('user_agent'),
            event.get('ip_address'),
            event.get('device')
        )
    ]

    execute_values(cursor, insert_query, values)
    conn.commit()
    cursor.close()
    conn.close()