def generate_permutations(arr):
    result = []
    def permute(a, l):
        if l == len(a):
            result.append(a[:])
        else:
            for i in range(l, len(a)):
                a[l], a[i] = a[i], a[l]
                permute(a, l+1)
                a[l], a[i] = a[i], a[l]
    permute(arr, 0)
    return result


def tsp_brute_force(distance_matrix):
    n = len(distance_matrix)
    vertices = list(range(n))

    all_permutations = generate_permutations(vertices)

    best_length = float('inf')
    best_route = None

    for route in all_permutations:
        route_length = 0.0
        for i in range(len(route)-1):
            route_length += distance_matrix[route[i]][route[i+1]]
        if route_length < best_length:
            best_length = route_length
            best_route = route[:]

    return best_route, best_length


# Пример использования
if __name__ == "__main__":
    distance_matrix = [
        [0, 2, 9, 10, 5],
        [1, 0, 6, 4,  7],
        [15,7, 0, 8,  3],
        [6, 3, 12,0,  11],
        [9, 5,  2, 6,  0]
    ]

    best_route, best_length = tsp_brute_force(distance_matrix)
    print("Лучший найденный маршрут:", best_route)
    print("Его длина:", best_length)