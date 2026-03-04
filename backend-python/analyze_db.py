import os
import sys
from app.config.db_config import get_db_connection

def analyze_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. List all tables and row counts
    print("--- Tabla y Conteo de Filas ---")
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    """)
    tables = [r[0] for r in cur.fetchall()]
    
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"{table}: {count} filas")
    
    # 2. List foreign key relationships
    print("\n--- Relaciones de Claves Foráneas ---")
    cur.execute("""
        SELECT
            tc.table_name, 
            kcu.column_name, 
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema='public';
    """)
    rels = cur.fetchall()
    for rel in rels:
        print(f"{rel[0]}.{rel[1]} -> {rel[2]}.{rel[3]}")
    
    conn.close()

if __name__ == "__main__":
    # Ensure app module is in path
    sys.path.append(os.getcwd())
    analyze_db()
