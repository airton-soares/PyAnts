class Ant:
    def __init__(self, current_city):
        self.current_city = current_city
        self.route = [current_city]

    def walk(self, new_city):
        self.current_city = new_city
        self.route.append(new_city)
