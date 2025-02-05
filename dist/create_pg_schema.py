import os
import dotenv
import psycopg2

dotenv.load_dotenv('../.env-pg', override=True)

# Database connection details
DB_HOST = os.getenv("AIVEN_PG_HOST")
DB_PORT = os.getenv("AIVEN_PG_PORT")
DB_NAME = os.getenv("AIVEN_PG_DB_NAME")
DB_USER = os.getenv("AIVEN_PG_USER")
DB_PASSWORD = os.getenv("AIVEN_PG_PASSWORD")
SQL_FILE = "../sql/clickstream_schema.sql"

def execute_sql_file(filename):
    """Executes SQL from a file in the PostgreSQL database."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=os.environ.get('AIVEN_PG_HOST'),
            port=os.environ.get('AIVEN_PG_PORT'),
            dbname=os.environ.get('AIVEN_PG_DB_NAME'),
            user=os.environ.get('AIVEN_PG_USER'),
            password=os.environ.get('AIVEN_PG_PASSWORD'),
            sslmode="require"
        )
        cur = conn.cursor()

        # Read SQL file
        with open(filename, "r") as file:
            sql_content = file.read()

        # Execute SQL commands
        cur.execute(sql_content)
        conn.commit()

        print("✅ Schema applied successfully!")

    except Exception as e:
        print(f"❌ Error applying schema: {e}")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    execute_sql_file(SQL_FILE)
