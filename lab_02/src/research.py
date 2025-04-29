import matplotlib.pyplot as plt
import time
import random
from alg import *

NUM_MEASURE = 200


def generate_matrix(size):
    return [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]


def measure_time(matrix_size):
    a = generate_matrix(matrix_size)
    b = generate_matrix(matrix_size)

    start = time.process_time()
    for _ in range(NUM_MEASURE):
        standard_multiply(a, b)
    standard_time = (time.process_time() - start) / NUM_MEASURE

    start = time.process_time()
    for _ in range(NUM_MEASURE):
        winograd_multiply(a, b)
    winograd_time = (time.process_time() - start) / NUM_MEASURE

    start = time.process_time()
    for _ in range(NUM_MEASURE):
        optimized_winograd_multiply(a, b)
    optimized_time = (time.process_time() - start) / NUM_MEASURE

    return standard_time, winograd_time, optimized_time


def research():
    sizes = [5 * i for i in range(1, 21, 3)]
    results = {}

    with open('performance_results.txt', 'w') as file:
        file.write('Matrix Size, Standard, Winograd, Optimized Winograd\n')
        for size in sizes:
            standard_time, winograd_time, optimized_time = measure_time(size)
            results[size] = (standard_time, winograd_time, optimized_time)
            file.write(f'{size}, {standard_time}, {winograd_time}, {optimized_time}\n')

    return results

def plot_results(results):
    sizes = list(results.keys())
    standard_times = [results[size][0] for size in sizes]
    winograd_times = [results[size][1] for size in sizes]
    optimized_times = [results[size][2] for size in sizes]

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, standard_times, label='Стандартный алгоритм', marker='o')
    plt.plot(sizes, winograd_times, label='Алгоритм Винограда', marker='s')
    plt.plot(sizes, optimized_times, label='Оптимизированный алгоритм', marker='^')

    plt.title("Сравнение алгоритмов умножения матриц по времени выполнения")
    plt.xlabel("Размерность строки квадратной матрицы")
    plt.ylabel("Время выполнения в секундах")
    plt.legend()
    plt.grid(True)
    plt.savefig('performance_plot.png')
    plt.show()


if __name__ == '__main__':
    results = research()
    plot_results(results)