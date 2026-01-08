import psycopg2
import sys

def check_prod_db():
    conn_str = "postgresql://postgres.jjxusciiuvcjltkreozq:IAmTheMan!20040113!@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Check test
        cur.execute("SELECT id, name, total_questions FROM tests_test WHERE name = 'Non-Verbal IQ Test - Set 2';")
        test = cur.fetchone()
        if not test:
            print("❌ Test 'Non-Verbal IQ Test - Set 2' NOT FOUND")
            return
        
        print(f"✅ Found Test: {test[1]} (ID: {test[0]}, Total Questions in DB field: {test[2]})")
        
        # Check questions
        cur.execute("SELECT order, question_text FROM questions WHERE test_id = %s ORDER BY order;", (test[0],))
        questions = cur.fetchall()
        print(f"Questions found in DB: {len(questions)}")
        for q in questions:
            print(f"  - Order {q[0]}: {q[1][:30]}...")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    check_prod_db()
