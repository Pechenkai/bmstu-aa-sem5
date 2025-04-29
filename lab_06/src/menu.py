import sys
import numpy as np
from antcolony import ant_colony_tsp_with_resources
from bruteforce import tsp_brute_force
from helpfunc import generate_graph
from paramresearch import research_parameters
from timeresearch import run_experiment

ant_colony_params = \
    {
    "num_iterations": 10,
    "num_ants": 10,
    "alpha": 0.5,
    "rho": 0.5,
    "max_resources": 100.0
}


def input_matrix():
    size = int(input("Введите размер матрицы: "))
    print("Введите матрицу (построчно, элементы через пробел):")
    matrix = []
    for _ in range(size):
        row = list(map(float, input().split()))
        if len(row) != size:
            print(f"Ошибка: строка должна содержать {size} элементов.")
            return input_matrix()
        matrix.append(row)
    return np.array(matrix)


def generate_random_matrix():
    size = int(input("Введите размер матрицы: "))
    matrix = generate_graph(size)
    print("Сгенерированная матрица:")
    print(matrix)
    return matrix


def set_ant_colony_params():
    global ant_colony_params
    print("Текущие параметры муравьиного алгоритма:")
    for key, value in ant_colony_params.items():
        print(f"{key}: {value}")
    print("\nВведите новые значения (оставьте пустым для сохранения текущего значения):")
    for key in ant_colony_params:
        value = input(f"{key} ({ant_colony_params[key]}): ")
        if value:
            ant_colony_params[key] = float(value) if '.' in value else int(value)


def test_program():
    print("\nВыберите режим ввода матрицы:")
    print("1. Ручной ввод")
    print("2. Случайная генерация")
    choice = input("Ваш выбор: ")
    if choice == "1":
        matrix = input_matrix()
    elif choice == "2":
        matrix = generate_random_matrix()
    else:
        print("Неверный выбор.")
        return

    print("\nВыберите алгоритм:")
    print("1. Полный перебор")
    print("2. Муравьиный алгоритм")
    choice = input("Ваш выбор: ")
    if choice == "1":
        result = tsp_brute_force(matrix)
        print("Результат полного перебора:", result)
    elif choice == "2":
        set_ant_colony_params()
        result = ant_colony_tsp_with_resources(matrix, **ant_colony_params)
        print("Результат муравьиного алгоритма:", result)
    else:
        print("Неверный выбор.")


def menu():
    while True:
        print("\n--- Меню ---")
        print("1. Тестировать программу")
        print("2. Исследование времени выполнения")
        print("3. Исследование параметризации")
        print("4. Настройка параметров муравьиного алгоритма")
        print("5. Выход")

        choice = input("Ваш выбор: ")

        if choice == "1":
            test_program()
        elif choice == "2":
            print("Запуск исследования времени выполнения...")
            run_experiment()
        elif choice == "3":
            print("Запуск исследования параметризации...")
            fraph = generate_graph(10)
            graphs = []
            graphs.append(fraph)

            research_parameters(graphs, M=10, output_filename="pvm22u265/application/param_results.tex")
        elif choice == "4":
            set_ant_colony_params()
        elif choice == "5":
            print("Выход из программы.")
            sys.exit(0)
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    menu()
