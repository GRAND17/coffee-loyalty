from services import add_customer, process_visit, get_customer_info
from db import create_table
import os

def clear_screen():
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Печатает шапку приложения"""
    print("=" * 50)
    print("☕  COFFEE LOYALTY - СИСТЕМА СКИДОК ДЛЯ КОФЕЙНИ  ☕")
    print("=" * 50)

def print_menu():
    """Печатает меню команд"""
    print("\n📋 ДОСТУПНЫЕ КОМАНДЫ:")
    print("  1. reg Имя Телефон  - зарегистрировать нового гостя")
    print("  2. check Телефон     - отметить визит (+1 кофе)")
    print("  3. info Телефон      - показать информацию о госте")
    print("  4. list              - показать всех гостей")
    print("  5. clear             - очистить экран")
    print("  6. exit              - выйти из программы")
    print("-" * 50)

def list_all_customers():
    """Показывает всех клиентов"""
    import sqlite3
    import os
    
    DB_PATH = os.path.join(os.path.dirname(__file__), "coffee.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, phone, visit_count, discount FROM customers ORDER BY visit_count DESC')
    customers = cursor.fetchall()
    conn.close()
    
    if not customers:
        print("\n📭 База данных пуста. Зарегистрируйте первого гостя!")
        return
    
    print("\n" + "=" * 60)
    print("📊 ВСЕ ГОСТИ (отсортированы по количеству визитов)")
    print("=" * 60)
    print(f"{'Имя':<20} {'Телефон':<15} {'Визитов':<10} {'Скидка':<10}")
    print("-" * 60)
    
    for customer in customers:
        name, phone, visits, discount = customer
        # Обрезаем имя, если слишком длинное
        if len(name) > 18:
            name = name[:15] + "..."
        print(f"{name:<20} {phone:<15} {visits:<10} {discount}%")
    
    print("=" * 60)
    print(f"Всего гостей: {len(customers)}")

def main():
    """Главная функция приложения"""
    # Создаём таблицу при запуске
    create_table()
    
    clear_screen()
    print_header()
    print_menu()
    
    while True:
        cmd = input("\n👉 Введите команду: ").strip()
        
        if cmd.lower() == 'exit':
            print("\n👋 До свидания! Хорошего дня!")
            break
        
        if cmd.lower() == 'clear':
            clear_screen()
            print_header()
            print_menu()
            continue
        
        if cmd.lower() == 'list':
            list_all_customers()
            continue
        
        if cmd.lower() == 'help':
            print_menu()
            continue
        
        # Разбираем команды с аргументами
        parts = cmd.split(maxsplit=2)
        
        if len(parts) < 2:
            print("❌ Неверный формат команды. Введите 'help' для списка команд.")
            continue
        
        action = parts[0].lower()
        
        if action == 'reg':
            if len(parts) == 3:
                name, phone = parts[1], parts[2]
                result = add_customer(name, phone)
                print(f"\n{result}")
            else:
                print("❌ Формат: reg Имя Телефон")
                print("   Пример: reg Анна +79161234567")
        
        elif action == 'check':
            phone = parts[1]
            result = process_visit(phone)
            print(f"\n{result}")
        
        elif action == 'info':
            phone = parts[1]
            info = get_customer_info(phone)
            if info:
                print("\n" + "=" * 40)
                print("📋 ИНФОРМАЦИЯ О ГОСТЕ")
                print("=" * 40)
                print(info)
                print("=" * 40)
            else:
                print(f"\n❌ Гость с номером {phone} не найден")
        
        else:
            print(f"❌ Неизвестная команда '{action}'. Введите 'help' для списка команд.")

if __name__ == "__main__":
    main()