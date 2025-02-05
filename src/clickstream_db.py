import os
import dotenv
import psycopg2
from psycopg2.extras import execute_values

dotenv.load_dotenv('../.env-pg', override=True)

def get_db_connection():
    conn = psycopg2.connect(os.environ.get("AIVEN_PG_URI"))
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

    try:
        execute_values(cursor, insert_query, values)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def write_session_stats_to_db(session_id, stats):
    conn = get_db_connection()
    cursor = conn.cursor()

    upsert_query = """
    INSERT INTO clickstream_session_stats (
        session_id,
        page_views,
        button_clicks
    ) VALUES (%s, %s, %s)
    ON CONFLICT (session_id) DO UPDATE SET
        page_views = EXCLUDED.page_views,
        button_clicks = EXCLUDED.button_clicks
    """

    try:
        cursor.execute(
            upsert_query,
            (
                session_id,
                stats['page_views'],
                stats['button_clicks']
            )
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()