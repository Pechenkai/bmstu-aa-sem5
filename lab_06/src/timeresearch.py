import time
import matplotlib.pyplot as plt
import pandas as pd
from bruteforce import tsp_brute_force
from antcolony import ant_colony_tsp_with_resources
from helpfunc import generate_graph

NUM_EXP = 50


def run_experiment():
    matrix_sizes = [2, 3, 4, 5, 6, 7, 8]

    results = []


    for size in matrix_sizes:
        matrix = generate_graph(size)
        sum_bf = 0
        sum_ant = 0

        for _ in range(NUM_EXP):
            start_time = time.time()
            tsp_brute_force(matrix)
            brute_force_time = time.time() - start_time

            sum_bf += brute_force_time

            start_time = time.time()
            ant_colony_tsp_with_resources(matrix)
            ant_colony_time = time.time() - start_time

            sum_ant += ant_colony_time

        results.append({
            "Matrix Size": size,
            "Brute Force Time (s)": sum_bf / NUM_EXP,
            "Ant Colony Time (s)": sum_ant / NUM_EXP
        })

    df = pd.DataFrame(results)
    create_latex_table(df)

    plot_results(df)


def create_latex_table(df):
    latex_table = df.to_latex(index=False, float_format="%.5f")
    with open("results_table.tex", "w") as f:
        f.write(latex_table)
    print("Таблица LaTeX сохранена в файл 'results_table.tex'.")


def plot_results(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df["Matrix Size"], df["Brute Force Time (s)"], label="Полный перебор", marker="o")
    plt.plot(df["Matrix Size"], df["Ant Colony Time (s)"], label="Муравьиный алгоритм", marker="o")
    plt.xlabel("Размерность матрицы")
    plt.ylabel("Время выполнения (сек)")
    plt.title("Зависимость времени выполнения от размера матриц")
    plt.legend()
    plt.grid()
    plt.savefig("execution_time_plot.png")
    plt.show()


if __name__ == "__main__":
    run_experiment()