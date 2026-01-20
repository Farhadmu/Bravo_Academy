import os
import sys
import django
from django.db import connection

# Manually add the apps directory to sys.path if needed
# (Already handled in base.py settings usually, but we need settings loaded first)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

def test_db_connection():
    print("Attempting to connect to the database...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
            if row:
                print("✅ Database connection successful! Query returned: 1")
            else:
                print("❌ Database connection failed: No data returned.")
    except Exception as e:
        print(f"❌ Database connection failed with error: {e}")

if __name__ == "__main__":
    test_db_connection()
