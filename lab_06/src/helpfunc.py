import numpy as np

def write_matrix_to_latex(matrix, filename):
    """
    Записывает матрицу в файл в формате LaTeX.

    matrix: list[list[int]]
        Матрица для записи.
    filename: str
        Имя файла для сохранения.
    """
    with open(filename, 'w') as f:
        f.write(r"\[" + "\n")  # Начало математического окружения
        f.write(r"\begin{bmatrix}" + "\n")

        # Запись строк матрицы
        for row in matrix:
            row_str = " & ".join(map(str, row))  # Преобразуем числа в строку, разделённые "&"
            f.write(row_str + r" \\" + "\n")  # Добавляем "\\" в конце каждой строки

        # Конец bmatrix и математического окружения
        f.write(r"\end{bmatrix}" + "\n")
        f.write(r"\]" + "\n")

def generate_graph(n, mean=10, std_dev=5, seed=None):
    if seed is not None:
        np.random.seed(seed)

    upper_triangle = np.random.normal(loc=mean, scale=std_dev, size=(n, n))

    upper_triangle = np.abs(upper_triangle)

    np.fill_diagonal(upper_triangle, 0)

    adjacency_matrix = np.triu(upper_triangle) + np.triu(upper_triangle, 1).T

    adjacency_matrix_int = adjacency_matrix.round().astype(int)

    adjacency_list = adjacency_matrix_int.tolist()

    return adjacency_list


# Пример использования:
if __name__ == "__main__":
    n = 5
    mean = 20
    std_dev = 10
    directed = False

    graph = generate_graph(n, mean, std_dev, seed=2)
    print("Матрица связности графа:")
    print(graph)