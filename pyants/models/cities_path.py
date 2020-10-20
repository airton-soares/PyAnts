import math


class CitiesPath:
    def __init__(self, city_1, city_2):
        self.city_1 = city_1
        self.city_2 = city_2
        self.length = math.sqrt((city_1.x - city_2.x)**2 + (city_1.y - city_2.y)**2)
        self.pheromone = 0
        self.passing_ants = []

    def get_adjacent_city(self, city):
        if self.city_1 == city:
            return self.city_2
        elif self.city_2 == city:
            return self.city_1
        else:
            return None

    def is_a_possible_path(self, city, route, cities_qty):
        if self.city_1 == city:
            return self.city_2 not in route or (cities_qty == len(route) and self.city_2 == route[0])
        elif self.city_2 == city:
            return self.city_1 not in route or (cities_qty == len(route) and self.city_1 == route[0])
        else:
            return False
