import random as r
import time as t
import matplotlib.pyplot as plt
import string
from alg import *

NUM_MEASUREMENTS = 200


def generate_random_word(length):
    return ''.join(r.choices(string.ascii_lowercase, k=length))


def measure_time(func, str1, str2):
    start_time = t.process_time()
    func(str1, str2)
    end_time = t.process_time()
    return end_time - start_time

# funcs = [levenshtein_recursive, levenshtein_recursive_memo, levenshtein, damerau_levenshtein]
funcs = [levenshtein, damerau_levenshtein]

def run_research(sizes):
    times = [[] for _ in range(len(funcs))]

    for i, func in enumerate(funcs):

        for size in sizes:
            time_total = 0

            print("func {} size {}".format(func.__name__, size))

            for _ in range(NUM_MEASUREMENTS):
                str1 = generate_random_word(size)
                str2 = generate_random_word(size)

                time_total += measure_time(func, str1, str2)

            times[i].append(time_total / NUM_MEASUREMENTS)

    return times


def plot_results(sizes, times):
    plt.figure()

    # func_names = ["Рек Левенштейн", "Рек Левенштейн c мем", "Нерек Левенштейн", "Нерек Дамерау - Левенштейн"]
    func_names = ["Нерек Левенштейн", "Нерек Дамерау - Левенштейн"]

    for i, func in enumerate(funcs):
        plt.plot(sizes, times[i], marker='o', label=func_names[i])

    plt.xlabel('Размер слов')
    plt.ylabel('Время (секунды)')
    plt.title('Сравнение нерекурсивных алгоритмов')
    plt.legend()
    plt.grid()
    # plt.show()
    plt.savefig("graph2.png")

def main():
    # sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sizes = [10, 20, 30, 40, 50, 100, 150, 200, 300, 400, 500]

    times = run_research(sizes)

    with open("res2.txt", "w") as f:
        f.write(str(times))
        f.write("\n")
    # for fu
    plot_results(sizes, times)

if __name__ == '__main__':
    main()