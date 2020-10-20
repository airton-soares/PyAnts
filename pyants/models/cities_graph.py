class CitiesGraph:
    def __init__(self, cities_paths):
        self.cities_paths = cities_paths

    def possible_paths(self, ant, cities_qty):
        return [city_path for city_path in self.cities_paths if city_path.is_a_possible_path(ant.current_city, ant.route, cities_qty)]
