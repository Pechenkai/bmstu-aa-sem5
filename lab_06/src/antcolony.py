import numpy as np
import random


def ant_colony_tsp_with_resources(distance_matrix,
                                  num_ants=10,
                                  num_iterations=10,
                                  alpha=0.5,
                                  beta=0.5,
                                  rho=0.5,
                                  tau_0=0.01,
                                  max_resources=100.0):
    n = len(distance_matrix)

    total_dist = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                total_dist += distance_matrix[i][j]
    Q = total_dist / n

    pheromone = [[tau_0 for _ in range(n)] for _ in range(n)]
    eta = [[0 if distance_matrix[i][j] == 0 else 1.0 / distance_matrix[i][j] for j in range(n)] for i in range(n)]

    best_route = None
    best_length = float('inf')

    for iteration in range(num_iterations):
        all_routes = []
        all_lengths = []

        for ant in range(num_ants):
            start = ant % n
            visited = [False] * n
            visited[start] = True
            route = [start]
            current = start

            remaining_resources = max_resources

            while len(route) < n:

                candidates = []
                for j in range(n):
                    if not visited[j]:
                        cost = distance_matrix[current][j]
                        if remaining_resources - cost >= 0:
                            val = (pheromone[current][j] ** alpha) * (eta[current][j] ** beta)
                            candidates.append((j, val))

                if len(candidates) == 0:
                    break

                denom = sum(val for _, val in candidates)
                if denom < 1e-12:
                    print(denom)
                    denom = 1

                r = random.random()
                cumulative = 0.0
                next_city = None
                for (city, val) in candidates:
                    p = val / denom
                    cumulative += p
                    if r <= cumulative:
                        next_city = city
                        break

                visited[next_city] = True
                route.append(next_city)

                cost = distance_matrix[current][next_city]
                remaining_resources -= cost
                current = next_city

            route_length = 0.0
            for i in range(len(route) - 1):
                route_length += distance_matrix[route[i]][route[i + 1]]

            all_routes.append(route)
            all_lengths.append(route_length)

            if route_length < best_length:
                best_length = route_length
                best_route = route[:]


        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1 - rho)
                if pheromone[i][j] < 1e-12:
                    pheromone[i][j] = 1e-12

        for k, route in enumerate(all_routes):
            route_length = all_lengths[k]
            if route_length > 0:
                delta = Q / route_length
            else:
                delta = Q
            for i in range(len(route) - 1):
                a, b = route[i], route[i + 1]
                pheromone[a][b] += delta
                pheromone[b][a] += delta

    return best_route, best_length


# Пример использования:
if __name__ == "__main__":
    distance_matrix = [
        [0, 2, 9, 10, 5],
        [1, 0, 6, 4, 7],
        [15, 7, 0, 8, 3],
        [6, 3, 12, 0, 11],
        [9, 5, 2, 6, 0]
    ]
    best_route, best_length = ant_colony_tsp_with_resources(distance_matrix,
                                                            num_ants=20,
                                                            num_iterations=3,
                                                            alpha=1,
                                                            beta=2,
                                                            rho=0.5,
                                                            tau_0=0.01,
                                                            max_resources=30.0)
    print("Лучший найденный маршрут:", best_route)
    print("Его длина:", best_length)
