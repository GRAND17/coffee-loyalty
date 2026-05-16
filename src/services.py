import sqlite3
import re
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'coffee.db')

def format_phone(raw_phone: str) -> str:
    digits = re.sub(r'\D', '', raw_phone)
    if len(digits) == 11 and digits.startswith('8'):
        return '+7' + digits[1:]
    elif len(digits) == 11 and digits.startswith('7'):
        return '+' + digits
    elif len(digits) == 10:
        return '+7' + digits
    return digits

def calculate_discount(visits: int) -> int:
    if visits < 5:
        return 0
    elif visits < 10:
        return 5
    else:
        return 10

def add_customer(name: str, phone: str):
    phone = format_phone(phone)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO customers (name, phone, visit_count, discount) VALUES (?, ?, 0, 0)',
            (name, phone)
        )
        conn.commit()
        conn.close()
        return f"✅ Клиент {name} ({phone}) успешно зарегистрирован!"
    except sqlite3.IntegrityError:
        conn.close()
        return f"⚠️ Клиент с номером {phone} уже существует в базе."

def process_visit(phone: str):
    phone = format_phone(phone)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers WHERE phone = ?', (phone,))
    customer = cursor.fetchone()
    if not customer:
        conn.close()
        return f"❌ Клиент с номером {phone} не найден."
    new_count = customer[3] + 1
    new_discount = calculate_discount(new_count)
    cursor.execute(
        'UPDATE customers SET visit_count = ?, discount = ? WHERE phone = ?',
        (new_count, new_discount, phone)
    )
    conn.commit()
    conn.close()
    return f"☕ Визит засчитан!\n👤 {customer[2]}\n🔢 Всего визитов: {new_count}\n💰 Текущая скидка: {new_discount}%"

def get_customer_info(phone: str):
    phone = format_phone(phone)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers WHERE phone = ?', (phone,))
    customer = cursor.fetchone()
    conn.close()
    if not customer:
        return None
    visits = customer[3]
    discount = customer[4]
    if visits < 5:
        visits_to_next = 5 - visits
        next_level = "5%"
    elif visits < 10:
        visits_to_next = 10 - visits
        next_level = "10%"
    else:
        visits_to_next = 0
        next_level = "максимальная скидка"
    return (
        f"👤 Имя: {customer[2]}\n"
        f"📞 Телефон: {customer[1]}\n"
        f"☕ Всего визитов: {visits}\n"
        f"💸 Текущая скидка: {discount}%\n"
        f"🎯 До следующего уровня: {visits_to_next} визитов ({next_level})"
    )