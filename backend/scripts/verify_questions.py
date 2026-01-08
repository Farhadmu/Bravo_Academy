import psycopg2
import sys

def verify_count():
    conn_str = "postgresql://postgres.jjxusciiuvcjltkreozq:IAmTheMan!20040113!@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require&connect_timeout=10"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        cur.execute("SELECT id, name, total_questions FROM tests WHERE name = 'Non-Verbal IQ Test - Set 2';")
        test = cur.fetchone()
        if not test:
            print("❌ Test not found")
            return
            
        print(f"✅ Found Test: {test[1]}")
        
        cur.execute("SELECT count(*) FROM questions WHERE test_id = %s;", (test[0],))
        count = cur.fetchone()[0]
        print(f"📊 Question count in DB: {count}")
        print(f"📄 Test field 'total_questions': {test[2]}")
        
        cur.close()
        conn.close()
        
        if count == 15:
            print("✨ SUCCESS: All 15 questions are live!")
        else:
            print(f"⚠️ Still at {count} questions.")
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    verify_count()
