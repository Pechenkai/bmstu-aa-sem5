def standard_multiply(a, b):
    rows_a = len(a)
    rows_b = len(b)

    if rows_a == 0 or rows_b == 0:
        return None

    cols_a = len(a[0])
    cols_b = len(b[0])

    if cols_a != rows_b or cols_a == 0 or cols_b == 0:
        return None

    c = [[0] * cols_b for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                c[i][j] += a[i][k] * b[k][j]

    return c


def winograd_multiply(a, b):
    rows_a = len(a)
    rows_b = len(b)

    if rows_a == 0 or rows_b == 0:
        return None

    cols_a = len(a[0])
    cols_b = len(b[0])

    if cols_a != rows_b or cols_a == 0 or cols_b == 0:
        return None

    c = [[0] * cols_b for _ in range(rows_a)]

    row_factor = [0] * rows_a
    col_factor = [0] * cols_b

    for i in range(rows_a):
        for j in range(cols_a // 2):
            row_factor[i] += a[i][2 * j] * a[i][2 * j + 1]

    for i in range(cols_b):
        for j in range(rows_b // 2):
            col_factor[i] += b[2 * j][i] * b[2 * j + 1][i]

    for i in range(rows_a):
        for j in range(cols_b):
            c[i][j] += -row_factor[i] - col_factor[j]

            for k in range(cols_a // 2):
                c[i][j] += (a[i][2 * k] + b[2 * k + 1][j]) * (a[i][2 * k + 1] + b[2 * k][j])

    if cols_a % 2 != 0:
        for i in range(rows_a):
            for j in range(cols_b):
                c[i][j] += a[i][cols_a - 1] * b[rows_b - 1][j]

    return c


def optimized_winograd_multiply(a, b):
    rows_a = len(a)
    rows_b = len(b)

    if rows_a == 0 or rows_b == 0:
        return None

    cols_a = len(a[0])
    cols_b = len(b[0])

    if cols_a != rows_b or cols_a == 0 or cols_b == 0:
        return None

    c = [[0] * cols_b for _ in range(rows_a)]

    row_factor = [0] * rows_a
    col_factor = [0] * cols_b

    for i in range(rows_a):
        j = cols_a // 2 - 1
        while j >= 0:
            row_factor[i] += a[i][j << 1] * a[i][(j << 1) + 1]
            j -= 1

    for i in range(cols_b):
        j = rows_b // 2 - 1
        while j >= 0:
            col_factor[i] += b[j << 1][i] * b[(j << 1) + 1][i]
            j -= 1

    for i in range(rows_a):
        for j in range(cols_b):
            c[i][j] += -row_factor[i] - col_factor[j]

            for k in range(cols_a // 2):
                c[i][j] += (a[i][k << 1] + b[(k << 1) + 1][j]) * (a[i][(k << 1) + 1] + b[k << 1][j])

            if cols_a % 2 != 0:
                c[i][j] += a[i][cols_a - 1] * b[rows_b - 1][j]

    return c


if __name__ == "__main__":
    mat_a = [[1, 2, 3, 6], [4, 5, 6, 7]]
    mat_b = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]

    # print(winograd_multiply(A, B))

    print(standard_multiply(mat_a, mat_b))
    print(winograd_multiply(mat_a, mat_b))
    print(optimized_winograd_multiply(mat_a, mat_b))
    #
    print(standard_multiply(mat_a, mat_b) == winograd_multiply(mat_a, mat_b))
    print(standard_multiply(mat_a, mat_b) == optimized_winograd_multiply(mat_a, mat_b))
