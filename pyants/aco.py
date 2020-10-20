from numpy.random import choice
from models.colony import Colony
import math


def optimize(cities_graph, cities, evaporation_rate, alpha, beta, colony_size, max_num_iterations, min_max):
    shortest_route = None

    for i in range(max_num_iterations):
        colony = Colony(colony_size, cities)

        for ant in colony.ants:
            move_ant(ant, cities_graph, alpha, beta, len(cities))

            if shortest_route is None or route_length(shortest_route) > route_length(ant.route):
                shortest_route = ant.route

        update_pheromones(cities_graph.cities_paths, evaporation_rate, min_max, shortest_route, len(cities))

    return shortest_route, route_length(shortest_route)


def move_ant(ant, cities_graph, alpha, beta, cities_qty):
    while True:
        possible_paths = cities_graph.possible_paths(ant, cities_qty)

        if not possible_paths:
            break

        chosen_path = choose_path(possible_paths, alpha, beta)
        chosen_path.passing_ants.append(ant)
        ant.walk(chosen_path.get_adjacent_city(ant.current_city))


def choose_path(possible_paths, alpha, beta):
    denominator = sum(
        [cities_path.pheromone**alpha * (1 / cities_path.length)**beta for cities_path in possible_paths]
    )

    if denominator == 0:
        probability_distribution = [1 / len(possible_paths) for _ in possible_paths]
    else:
        probability_distribution = [
            (cities_path.pheromone**alpha * (1 / cities_path.length)**beta) / denominator
            for cities_path in possible_paths]

    return choice(possible_paths, 1, p=probability_distribution)[0]


def route_length(route):
    length = 0

    for i in range(0, len(route) - 1):
        partial_distance = math.sqrt((route[i].x - route[i + 1].x)**2 + (route[i].y - route[i + 1].y)**2)
        length += partial_distance

    return length


def update_pheromones(cities_paths, evaporation_rate, min_max, shortest_route, cities_qtd):
    for cities_path in cities_paths:
        if min_max:
            shortest_route_length = route_length(shortest_route)
            max_pheromone = (1 / evaporation_rate) * (1 / shortest_route_length)
            min_pheromone = max_pheromone / (2 * cities_qtd)
            new_pheromone = (1 - evaporation_rate) * cities_path.pheromone + (1 / shortest_route_length)

            if new_pheromone < min_pheromone:
                cities_path.pheromone = min_pheromone
            elif new_pheromone > max_pheromone:
                cities_path.pheromone = max_pheromone
            else:
                cities_path.pheromone = new_pheromone
        else:
            heuristic_sum = sum([1 / route_length(ant.route) for ant in cities_path.passing_ants])
            cities_path.pheromone = (1 - evaporation_rate) * cities_path.pheromone + heuristic_sum

        cities_path.passing_ants = []
