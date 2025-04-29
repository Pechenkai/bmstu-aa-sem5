import random
import matplotlib.pyplot as plt
from alg import *
# Константное значение размера массива
ARRAY_SIZE = 1023


def initialize_random_array(size):
    return random.sample(range(1, 10001), size)


def gather_comparison_data(arr):
    comparisons_linear = []
    comparisons_binary = []

    sorted_arr = sorted(arr)

    for idx in range(len(arr)):
        target = arr[idx]

        _, linear_comparisons = search_linear(arr, target)
        comparisons_linear.append(linear_comparisons)

        target = sorted_arr[idx]
        _, binary_comparisons = search_binary(sorted_arr, target)
        comparisons_binary.append(binary_comparisons)

    return comparisons_linear, comparisons_binary


def plot_histograms(comparisons_linear, comparisons_binary):
    indices = list(range(len(comparisons_linear)))

    # print(comparisons_linear)

    plt.figure(figsize=(6, 6))
    plt.bar(indices, comparisons_linear, color='blue')
    plt.title('Количество сравнений (Линейный поиск)')
    plt.xlabel('Индекс элемента')
    plt.ylabel('Количество сравнений')
    plt.savefig("ls.png")
    plt.close()

    plt.figure(figsize=(6, 6))
    plt.bar(indices, comparisons_binary, color='green')
    plt.title('Количество сравнений (Бинарный поиск)')
    plt.xlabel('Индекс элемента')
    plt.ylabel('Количество сравнений')
    plt.savefig("bs.png")
    plt.close()

    plt.figure(figsize=(6, 6))
    plt.bar(indices, sorted(comparisons_binary), color='red')
    plt.title('Количество сравнений (Бинарный поиск) отсортированный')
    plt.xlabel('Индекс элемента')
    plt.ylabel('Количество сравнений')
    plt.savefig("bs_sort.png")
    plt.close()


def main_research():
    random_array = initialize_random_array(ARRAY_SIZE)

    comparisons_linear, comparisons_binary = gather_comparison_data(random_array)

    plot_histograms(comparisons_linear, comparisons_binary)


if __name__ == "__main__":
    main_research()