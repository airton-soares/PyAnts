from models.ant import Ant
import random


class Colony:
    def __init__(self, colony_size, cities):
        self.ants = [Ant(random.choice(cities)) for _ in range(colony_size)]
