import statistics
from helpfunc import generate_graph, write_matrix_to_latex
from antcolony import ant_colony_tsp_with_resources
from bruteforce import tsp_brute_force

def research_parameters(graphs, M=10, output_filename="results.tex"):
    alpha_values = [0.1, 0.25, 0.5, 0.75, 0.9]
    rho_values = [0.1, 0.25, 0.5, 0.75, 0.9]
    tmax_values = [100, 200, 300, 400, 500]

    # Вычисляем оптимальные длины для всех графов
    best_lengths = []
    for g in graphs:
        _, best_len = tsp_brute_force(g)
        best_lengths.append(best_len)

    results = []

    # Параметры для исследования
    for alpha in alpha_values:
        beta = 1 - alpha
        for rho in rho_values:
            for tmax in tmax_values:
                row = [alpha, beta, rho, tmax]

                # Исследуем каждый граф
                for graph_index, g in enumerate(graphs):
                    best_len = best_lengths[graph_index]
                    deviations = []
                    for _ in range(M):
                        _, route_len = ant_colony_tsp_with_resources(
                            g,
                            num_iterations=tmax,
                            alpha=alpha,
                            beta=beta,
                            rho=rho
                        )
                        diff = route_len - best_len
                        deviations.append(diff)

                    if deviations:
                        max_dev = max(deviations)
                        median_dev = statistics.median(deviations)
                        mean_dev = statistics.mean(deviations)
                    else:
                        max_dev = 0
                        median_dev = 0
                        mean_dev = 0

                    # Добавляем статистику для текущего графа
                    row.extend([max_dev, median_dev, mean_dev])

                results.append(row)

    write_results_to_latex(results, output_filename)


def write_results_to_latex(results, filename):
    with open(filename, 'w') as f:
        f.write(r"""\documentclass{article}
        \usepackage{amsmath, booktabs, longtable}
        \RequirePackage[utf8]{inputenc}
        \RequirePackage[T2A]{fontenc}
        \usepackage[english,russian]{babel}
        \begin{document}
        \centering
        \begin{longtable}{ccc|ccc|ccc|ccc}
        \caption{Результаты параметризации муравьиного алгоритма (начало)} \\ % Заголовок для первой страницы
        \toprule
        $\alpha$ & $\rho$ & $t_{\max}$ & \multicolumn{3}{c|}{Graph 1} & \multicolumn{3}{c|}{Graph 2} & \multicolumn{3}{c}{Graph 3} \\
         & & & Max & Med & Mean & Max & Med & Mean & Max & Med & Mean \\
        \midrule
        \endfirsthead
        \caption[]{Результаты параметризации муравьиного алгоритма (продолжение)} \\ % Заголовок для промежуточных страниц
        \toprule
        $\alpha$ & $\rho$ & $t_{\max}$ & \multicolumn{3}{c|}{Graph 1} & \multicolumn{3}{c|}{Graph 2} & \multicolumn{3}{c}{Graph 3} \\
         & & & Max & Med & Mean & Max & Med & Mean & Max & Med & Mean \\
        \midrule
        \endhead
        \bottomrule
        \endfoot
        """)

        for row in results:
            alpha, beta, rho, tmax = row[:4]
            metrics = row[4:]
            metrics_str = " & ".join([f"{m:.2f}" for m in metrics])
            f.write(f"{alpha} & {rho} & {tmax} & {metrics_str} \\\\ \n")

        f.write(r"\bottomrule" + "\n")
        f.write(r"\end{longtable}" + "\n")
        f.write(r"\end{document}" + "\n")


if __name__ == "__main__":
    graph1 = generate_graph(10)
    graph2 = generate_graph(10)
    graph3 = generate_graph(10)

    graphs = [graph1, graph2, graph3]

    write_matrix_to_latex(graph1, "graph1.tex")
    write_matrix_to_latex(graph2, "graph2.tex")
    write_matrix_to_latex(graph3, "graph3.tex")


    research_parameters(graphs, M=10, output_filename="pvm22u265/application/param_results.tex")
    print("Исследование параметров завершено, результаты записаны в 'param_results.tex'.")