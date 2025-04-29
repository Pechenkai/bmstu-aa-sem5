from testing import *
from research import *

def menu():
    while True:
        print("\nМеню:")
        print("1. Выполнить")
        print("2. Протестировать")
        print("3. Исследование")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            perform_distance_calculation()
        elif choice == "2":
            run_tests()
        elif choice == "3":
            run_research()
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def perform_distance_calculation():
    print("\nВыберите функцию для нахождения расстояния между строками:")
    print("1. Левенштейн (рекурсивный)")
    print("2. Левенштейн (рекурсивный с мемоизвцией)")
    print("3. Левенштейн (нерекурсивный)")
    print("4. Дамерау-Левенштейн (нерекурсивный)")

    func_choice = input("Введите номер функции (1-4): ")

    if func_choice not in ["1", "2", "3", "4"]:
        print("Неверный выбор. Возвращаемся в главное меню.")
        return

    str1 = input("Введите первую строку: ")
    str2 = input("Введите вторую строку: ")

    if func_choice == "1":
        result = levenshtein_recursive(str1, str2)
    elif func_choice == "2":
        result = levenshtein_recursive_memo(str1, str2)
    elif func_choice == "3":
        result = levenshtein(str1, str2)
    elif func_choice == "4":
        result = damerau_levenshtein(str1, str2)

    print(f"Результат: расстояние между строками = {result}")


def run_tests():
    print("\nЗапуск тестов...")
    testing()
    print("Тестирование завершено.")


def run_research():
    print("\nЗапуск исследования...")
    main() # Вызов функции исследования
    print("Исследование завершено.")


if __name__ == "__main__":
    menu()