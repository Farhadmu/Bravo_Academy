import dj_database_url
import psycopg2
import os
import sys

def test_connection():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL not found in environment")
        sys.exit(1)
        
    print(f"DEBUG: Attempting connection to {db_url.split('@')[-1]}")
    try:
        config = dj_database_url.parse(db_url)
        conn = psycopg2.connect(
            dbname=config['NAME'],
            user=config['USER'],
            password=config['PASSWORD'],
            host=config['HOST'],
            port=config['PORT'],
            sslmode='require'
        )
        print("SUCCESS: Database connection established!")
        conn.close()
    except Exception as e:
        print(f"FAILURE: Could not connect to database. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
