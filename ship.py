# Ship Class
class Ship:
    def __init__(self, name, capacity, fuel, speed):
        self.name = name # Name of the ship
        self.capacity = capacity # Max number of passengers allowed on the ship
        self.fuel = fuel # Amount of fuel in gallons
        self.speed = speed # Speed of the ship in lightyears per hour

    # Prints a summary of the ship details
    def summary(self):
        return(
            f"{self.name:<15}{self.capacity:<15}{self.fuel:<15}{self.speed:<15}"
        )
