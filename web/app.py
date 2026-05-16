import sys
import os
from flask import Flask, render_template, request, redirect, url_for
from services import add_customer

app = Flask(__name__)
app.secret_key = 'coffee-secret-2026'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask, render_template
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'coffee.db')

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone, visit_count, discount FROM customers ORDER BY visit_count DESC')
    customers = cursor.fetchall()
    conn.close()
    return render_template('index.html', customers=customers)
    
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    
    if name and phone:
        add_customer(name, phone)
    
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    from db import create_table
    create_table()
    print("=" * 50)
    print("Открыть: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)
