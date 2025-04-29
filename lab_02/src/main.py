import sys
from testing import *
from research import *


def input_matrix(text):
    try:
        rows = int(input(f"Введите количество строк для {text}: "))
        cols = int(input(f"Введите количество столбцов для {text}: "))
        if rows <= 0 or cols <= 0:
            raise ValueError("Размер матрицы должен быть положительным числом.")

        matrix = []
        print(f"Введите элементы матрицы {text} (по строкам):")
        for i in range(rows):
            row = list(map(int, input(f"Строка {i + 1}: ").split()))
            if len(row) != cols:
                raise ValueError(f"Количество элементов в строке должно быть равно {cols}.")
            matrix.append(row)

        return matrix
    except ValueError as e:
        print(f"Ошибка ввода: {e}")
        return None


# Функция умножения матриц с выводом результатов
def multiply_matrices():
    print("Умножение матриц вручную:")
    A = input_matrix("матрицы A")
    if A is None:
        return
    B = input_matrix("матрицы B")
    if B is None:
        return

    if len(A[0]) != len(B):
        print("Ошибка: количество столбцов матрицы A должно быть равно количеству строк матрицы B.")
        return

    print("Результаты умножения матриц тремя способами:")
    print("Обычный алгоритм:")
    result_standard = standard_multiply(A, B)
    if result_standard is None:
        print("Ошибка: невозможно умножить матрицы.")
    else:
        for row in result_standard:
            print(row)

    print("Алгоритм Винограда:")
    result_winograd = winograd_multiply(A, B)
    if result_winograd is None:
        print("Ошибка: невозможно умножить матрицы.")
    else:
        for row in result_winograd:
            print(row)

    print("Оптимизированный алгоритм Винограда:")
    result_optimized = optimized_winograd_multiply(A, B)
    if result_optimized is None:
        print("Ошибка: невозможно умножить матрицы.")
    else:
        for row in result_optimized:
            print(row)


# Функция для запуска тестирования
def run_tests():
    print("Запуск тестирования...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMatrixMultiplication)
    unittest.TextTestRunner(verbosity=2).run(suite)


# Функция для исследования
def run_performance_test():
    print("Запуск исследования производительности...")
    results = research()
    plot_results(results)
    print("Исследование завершено. Результаты сохранены в файлы.")


# Главное меню
def main_menu():
    while True:
        print("\nМеню:")
        print("1. Умножить две матрицы")
        print("2. Провести тестирование")
        print("3. Провести исследование")
        print("4. Выход")

        try:
            choice = int(input("Выберите действие (1-4): "))
            if choice == 1:
                multiply_matrices()
            elif choice == 2:
                run_tests()
            elif choice == 3:
                run_performance_test()
            elif choice == 4:
                print("Выход из программы.")
                sys.exit()
            else:
                print("Ошибка: Введите число от 1 до 4.")
        except ValueError:
            print("Ошибка: Введите корректное число.")


if __name__ == '__main__':
    main_menu()
