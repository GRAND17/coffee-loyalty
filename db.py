import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "coffee.db")

def create_table():
    """Создаём таблицу customers, если её ещё нет"""
    print("Connecting to SQLite database...")
    
    # SQLite подключается к файлу (если файла нет - создаст)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Connected. Creating table...")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            visit_count INTEGER DEFAULT 0,
            discount INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Table 'customers' created!")
    print(f"📁 Database file: {DB_PATH}")

if __name__ == "__main__":
    create_table()