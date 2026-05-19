import sys
import os

# Добавляем путь к папке src/
SRC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
sys.path.insert(0, SRC_PATH)

from flask import Flask, render_template, request, redirect, url_for, flash

from services import add_customer, process_visit, get_customer_info
from db import create_table
import sqlite3

# Путь к базе данных
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'coffee.db')

app = Flask(__name__)
app.secret_key = 'coffee-secret-2026'

@app.route('/')
def index():
    """Главная страница со списком клиентов"""
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
        result = add_customer(name, phone)
        if '✅' in result:
            flash(result, 'success')
        else:
            flash(result, 'error')
    
    return redirect(url_for('index'))

@app.route('/check', methods=['POST'])
def check():
    phone = request.form.get('phone', '').strip()
    if phone:
        result = process_visit(phone)
        if '☕' in result:
            flash(result, 'success')
        elif '❌' in result:
            flash(result, 'error')
    return redirect(url_for('index'))

@app.route('/info', methods=['POST'])
def info():
    phone = request.form.get('phone', '').strip()
    if phone:
        result = get_customer_info(phone)
        if result:
            flash(result, 'info')
        else:
            flash(f'Гость с номером {phone} не найден', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    print("=" * 50)
    print("☕ Coffee Loyalty Web Server")
    print("Открыть: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)