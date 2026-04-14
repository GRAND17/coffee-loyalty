from services import add_customer, process_visit, get_customer_info
from db import create_table

def main():
    # Создаём таблицу (если ещё не создана)
    create_table()
    
    print("=" * 50)
    print("ТЕСТОВЫЙ РЕЖИМ КОФЕЙНИ (SQLite)")
    print("=" * 50)
    print("Команды:")
    print("  reg Имя Телефон  - зарегистрировать клиента")
    print("  check Телефон     - отметить визит")
    print("  info Телефон      - информация о клиенте")
    print("  exit              - выход")
    print("-" * 50)
    
    while True:
        cmd = input("\nВведите команду: ").strip()
        
        if cmd.lower() == 'exit':
            print("До свидания!")
            break
        
        parts = cmd.split(maxsplit=2)
        
        if len(parts) < 2:
            print("❌ Неверный формат команды")
            continue
        
        action = parts[0].lower()
        
        if action == 'reg':
            if len(parts) == 3:
                name, phone = parts[1], parts[2]
                result = add_customer(name, phone)
                print(result)
            else:
                print("❌ Формат: reg Имя Телефон")
        
        elif action == 'check':
            phone = parts[1]
            result = process_visit(phone)
            print(result)
        
        elif action == 'info':
            phone = parts[1]
            info = get_customer_info(phone)
            if info:
                print("\n" + "=" * 30)
                print(info)
                print("=" * 30)
            else:
                print(f"❌ Клиент с номером {phone} не найден")
        
        else:
            print("❌ Неизвестная команда. Используйте reg, check или info")

if __name__ == "__main__":
    main()