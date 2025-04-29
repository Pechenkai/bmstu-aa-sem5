import math as m


def levenshtein_recursive(str1, str2):
    len1 = len(str1)
    len2 = len(str2)

    if len1 == 0:
        return len2
    elif len2 == 0:
        return len1
    elif str1[0] == str2[0]:
        return levenshtein_recursive(str1[1:], str2[1:])

    return 1 + min(
        levenshtein_recursive(str1[1:], str2),
        levenshtein_recursive(str1, str2[1:]),
        levenshtein_recursive(str1[1:], str2[1:])
    )


def levenshtein_recursive_memo(str1, str2, cache_matrix=None):
    len1 = len(str1)
    len2 = len(str2)

    if cache_matrix is None:
        cache_matrix = [[-1] * (len2 + 1) for _ in range(len1 + 1)]

    idx_rows = len(cache_matrix) - len1 - 1
    idx_cols = len(cache_matrix[0]) - len2 - 1

    if len1 == 0:
        cache_matrix[idx_rows][idx_cols] = len2
        return len2
    elif len2 == 0:
        cache_matrix[idx_rows][idx_cols] = len1
        return len1
    elif str1[0] == str2[0]:
        curr = cache_matrix[idx_rows + 1][idx_cols + 1]
        return curr if curr != -1 else levenshtein_recursive_memo(str1[1:], str2[1:], cache_matrix)

    delete = cache_matrix[idx_rows + 1][idx_cols]
    add = cache_matrix[idx_rows][idx_cols + 1]
    swap = cache_matrix[idx_rows + 1][idx_cols + 1]

    return 1 + min(
        delete if delete != -1 else levenshtein_recursive_memo(str1[1:], str2, cache_matrix),
        add if add != -1 else levenshtein_recursive_memo(str1, str2[1:], cache_matrix),
        swap if swap != -1 else levenshtein_recursive_memo(str1[1:], str2[1:], cache_matrix)
    )


def levenshtein(str1, str2):
    len1 = len(str1)
    len2 = len(str2)

    cache_matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        cache_matrix[i][0] = i
    for j in range(len2 + 1):
        cache_matrix[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1

            cache_matrix[i][j] = min(
                cache_matrix[i - 1][j],
                cache_matrix[i][j - 1],
                cache_matrix[i - 1][j - 1]
            ) + cost

    return cache_matrix[-1][-1]


def damerau_levenshtein(str1, str2):
    len1 = len(str1)
    len2 = len(str2)

    cache_matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        cache_matrix[i][0] = i
    for j in range(len2 + 1):
        cache_matrix[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1

            cache_matrix[i][j] = min(
                cache_matrix[i - 1][j],
                cache_matrix[i][j - 1],
                cache_matrix[i - 1][j - 1]
            ) + cost

            if i > 1 and j > 1 and str1[i - 1] == str2[j - 2] and str1[i - 2] == str2[j - 1]:
                cache_matrix[i][j] = min(cache_matrix[i][j], cache_matrix[i - 2][j - 2] + 1)

    return cache_matrix[-1][-1]
