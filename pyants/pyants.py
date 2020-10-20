import os
import aco
import time
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from models.city import City
from models.cities_path import CitiesPath
from models.cities_graph import CitiesGraph


def build_args_parser():
    usage = 'python pyants.py -d <dimension>\n       ' \
            'run with --help for arguments descriptions'
    parser = ArgumentParser(description='A Python implementation of the Ant Colony Optimization algorithm to the'
                                        ' traveling salesman problem', usage=usage)
    parser.add_argument('-c', '--colony', dest='colony_size', type=int, default=30,
                        help='Size of the ant colony')
    parser.add_argument('-e', '--evaporation_rate', dest='evaporation_rate', type=float, default=0.3,
                        help='Evaporation rate of the pheromone')
    parser.add_argument('-a', '--alpha', dest='alpha', type=float, default=1,
                        help='Coefficient indicating the degree of importance that the amount of pheromone will have to'
                             ' determine the probability of choosing a path.')
    parser.add_argument('-b', '--beta', dest='beta', type=float, default=3,
                        help='Coefficient indicating the degree of importance that the path length will have to '
                             'determine the probability of choosing a path.')
    parser.add_argument('--min_max', action='store_true',
                        help='Defines either the MIN-MAX method will be used or not.')
    parser.add_argument('--input', dest='input_file_path', type=str, default="data/att48_xy.txt",
                        help='Input file with the coordinates of the cities')
    parser.add_argument('-i', '--iterations', dest='max_num_iterations', type=int, default=100,
                        help='Maximum number of iterations in the search')
    parser.add_argument('--simulations', dest='num_simulations', type=int, default=30,
                        help='Number of simulations to be done for the optimization')

    return parser


def build_cities_graph(input_file_path):
    input_file = open(input_file_path, 'r')
    lines = input_file.readlines()

    cities = []

    for i in range(len(lines)):
        coordinates = [int(coord.rstrip("\n")) for coord in lines[i].split(' ')]
        cities.append(City(coordinates, str(i + 1)))

    cities_qtd = len(lines)
    cities_paths = []

    for i in range(cities_qtd - 1):
        current_city = cities[i]
        cities_to_connect = cities[i + 1:]

        for city_to_connect in cities_to_connect:
            cities_paths.append(CitiesPath(current_city, city_to_connect))

    return CitiesGraph(cities_paths), cities


def print_route(route):
    route_str = ""
    routes_qty = len(route)

    for i in range(routes_qty):
        if i == routes_qty - 1:
            route_str += str(route[i].label)
        else:
            route_str += str(route[i].label) + ", "

    print("Rota: " + route_str)
    print("----------------------------------------------------------------------------------------------------")


def main():
    args_parser = build_args_parser()
    args = args_parser.parse_args()
    results_dir_path = "results"

    if not os.path.exists(results_dir_path):
        os.makedirs(results_dir_path)

    shortest_distance_list = []

    for i in range(args.num_simulations):
        start_time = time.time()

        cities_graph, cities = build_cities_graph(args.input_file_path)
        shortest_route, shortest_distance = aco.optimize(cities_graph, cities, args.evaporation_rate, args.alpha,
                                                         args.beta, args.colony_size, args.max_num_iterations,
                                                         args.min_max)

        elapsed_time = time.time() - start_time

        print("Simulação: " + str(i + 1) + ", Menor distância: " + str(round(shortest_distance, 2)) + "(" +
              str(round(elapsed_time, 2)) + " s)")
        print_route(shortest_route)

        shortest_distance_list.append(shortest_distance)

    plt.clf()
    plt.boxplot(shortest_distance_list)
    plt.ylabel("Menor distância")
    plt.title("Problema do caixeiro viajante usando ACO com " + str(args.colony_size) + " formigas")
    plt.savefig(os.path.join(results_dir_path, "shortest_distance_box_plot.png"), bbox_inches='tight')


if __name__ == '__main__':
    main()
