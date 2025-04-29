from testing import *
from research import *


def create_array(size, fill_method):
    arr = []
    if fill_method == 1:
        arr = [random.randint(1, 100) for _ in range(size)]
    elif fill_method == 2:
        print(f"Введите {size} элементов массива:")
        for i in range(size):
            try:
                arr.append(int(input(f"Введите {i + 1} элемент массива: ")))
            except ValueError:
                print("Введен некорректный элемент")
                return None
    return arr


def find_element():
    try:
        size = int(input("Введите размер массива: "))
    except ValueError:
        print("Должно быть введено целое число.")
        return
    else:
        if size < 1:
            print("Число должно быть положительным.")
            return

    fill_method = input("1 - заполнить массив случайными числами\n2 - ввести вручную.\nВвод: ")
    try:
        fill_method = int(fill_method)
    except ValueError:
        print("Должно быть введено целое число.")
        return
    else:
        if fill_method != 1 and fill_method != 2:
            print("Введена некорректная опция.")
            return

    arr = create_array(size, fill_method)

    if arr is None:
        return

    print("Массив: ", end="")
    for i in range(size):
        print(arr[i], end=", ")

    print()

    try:
        target = int(input("Введите элемент для поиска: "))
    except ValueError:
        print("Должно быть введено целое число.")
        return

    # Поиск элемент линейным поиском
    print("\nЛинейный поиск:")
    position_linear, comparisons_linear = search_linear(arr, target)
    if position_linear != -1:
        print(f"Элемент найден на позиции {position_linear}. Число сравнений: {comparisons_linear}")
    else:
        print(f"Элемент не найден. Число сравнений: {comparisons_linear}")

    # Поиск элемент бинарным поиском
    arr.sort()  # Массив должен быть отсортирован для бинарного поиска
    print("\nБинарный поиск (после сортировки массива):")
    position_binary, comparisons_binary = search_binary(arr, target)
    if position_binary != -1:
        print(f"Элемент найден на позиции {position_binary}. Число сравнений: {comparisons_binary}")
    else:
        print(f"Элемент не найден. Число сравнений: {comparisons_binary}")


def test_program():
    print("Запуск тестов...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchAlgorithms)
    unittest.TextTestRunner().run(suite)


def main():
    while True:
        print("\nМеню:")
        print("1) Найти элемент")
        print("2) Протестировать программу")
        print("2) Исследование")
        print("0) Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            find_element()
        elif choice == "2":
            test_program()
        elif choice == "3":
            main_research()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
