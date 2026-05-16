import sqlite3 
import os 
 
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'coffee.db') 
 
def create_table(): 
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor() 
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        phone TEXT UNIQUE NOT NULL, 
        name TEXT NOT NULL, 
        visit_count INTEGER DEFAULT 0, 
        discount INTEGER DEFAULT 0, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''' 
    ) 
    conn.commit() 
    conn.close() 
    print("Table created!") 
