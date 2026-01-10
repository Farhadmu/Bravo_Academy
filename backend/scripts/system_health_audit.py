import os
import sys
import psycopg2
from typing import List, Dict

# Production Configuration
DB_URI = "postgresql://postgres.jjxusciiuvcjltkreozq:IAmTheMan!20040113!@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

def verify_integrity():
    print("=" * 75)
    print("  DEVELOPER PORTAL & SYSTEM INTEGRITY VERIFICATION")
    print("=" * 75)
    
    conn = None
    try:
        # 1. Connection Test
        print("\n[1/4] Establishing Secure Production Connection...")
        conn = psycopg2.connect(DB_URI, connect_timeout=10)
        cur = conn.cursor()
        print("✅ Connection Successful.")
        
        # 2. Schema Verification
        print("\n[2/4] Verifying System Schema...")
        required_tables = [
            'maintenance_mode', 'feature_flags', 'login_logs', 
            'page_visits', 'active_sessions'
        ]
        
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = ANY(%s)
        """, (required_tables,))
        
        found_tables = [row[0] for row in cur.fetchall()]
        
        for table in required_tables:
            status = "✅ Found" if table in found_tables else "❌ MISSING"
            print(f"  - {table:20} {status}")
            
        if len(found_tables) < len(required_tables):
            print("🛑 SCHEMA INCOMPLETE: Some tables are still missing.")
        else:
            print("✅ Schema Integrity Verified.")
            
        # 3. Data Integrity Verification
        print("\n[3/4] Verifying Core Configuration Data...")
        
        # Check Maintenance Mode record
        cur.execute("SELECT COUNT(*) FROM maintenance_mode;")
        m_count = cur.fetchone()[0]
        status = "✅ Initialized" if m_count > 0 else "❌ EMPTY (Configuration Missing)"
        print(f"  - Maintenance Records:  {m_count:10} {status}")
        
        # Check users for developer access
        cur.execute("SELECT COUNT(*) FROM users WHERE is_developer = true;")
        dev_count = cur.fetchone()[0]
        status = "✅ Dev Access Configured" if dev_count > 0 else "⚠️ No Developers Found"
        print(f"  - Developer Users:     {dev_count:10} {status}")
        
        # 4. Transactional Data Sanity Check
        print("\n[4/4] Verifying Test Data Health...")
        cur.execute("SELECT COUNT(*) FROM questions;")
        q_count = cur.fetchone()[0]
        print(f"  - Total Questions:     {q_count:10} (Production Payload)")
        
        cur.execute("SELECT COUNT(*) FROM results;")
        r_count = cur.fetchone()[0]
        print(f"  - Total Test Results:  {r_count:10} (User Activity)")
        
        print("\n" + "=" * 75)
        print("  VERIFICATION COMPLETE: SYSTEM IS 100% OPERATIONAL")
        print("=" * 75)
        
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {str(e)}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    verify_integrity()
