# Ship Class
class Ship:
    def __init__(self, name, capacity, fuel, speed):
        self.name = name # Name of the ship
        self.capacity = capacity # Max number of passengers allowed on the ship
        self.fuel = fuel # Amount of fuel in gallons
        self.speed = speed # Speed of the ship in lightyears per hour

    @staticmethod
    def get_headers(show_number):
        if show_number:
            headers = ["Number", "Name", "Capacity", "Fuel", "Speed"]
            return f"{headers[0]:<10}{headers[1]:<15}{headers[2]:<15}{headers[3]:<15}{headers[4]:<15}"
        else:
            headers = ["Name", "Capacity", "Fuel", "Speed"]
            return f"{headers[0]:<15}{headers[1]:<15}{headers[2]:<15}{headers[3]:<15}"

    # Prints a summary of the ship details
    def summary(self):
        return(
            f"{self.name:<15}{self.capacity:<15}{self.fuel:<15}{self.speed:<15}"
        )
