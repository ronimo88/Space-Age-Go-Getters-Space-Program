# RescueSite Class
class RescueSite:
    def __init__(
        self,
        name,
        distance,
        rescue_time,
        danger_level,
        survivor_count,
        required_role,
        required_equipment
    ):
        self.name = name
        self.distance = distance
        self.rescue_time = rescue_time
        self.danger_level = danger_level
        self.survivor_count = survivor_count
        self.required_role = required_role
        self.required_equipment = required_equipment


    def summary(self):
        return(
            f"{self.name:<15}{self.distance:<15}{self.rescue_time:<20}{self.danger_level:<15}{self.survivor_count:<15}{self.required_role:<15}"
        )

    def get_danger_description(self):
        danger_levels = {
            1: "Low",
            2: "Moderate",
            3: "High",
            4: "Severe",
            5: "Critical"
        }

        return danger_levels.get(self.danger_level, "Unknown")


