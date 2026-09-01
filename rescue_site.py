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
        self.rescue_time = rescue_time # (1) Life Support Failure (2) Engine Failure (3) Missing Crew
        self.danger_level = danger_level
        self.survivor_count = survivor_count
        self.required_role = required_role
        self.required_equipment = required_equipment

    @staticmethod
    def get_headers(show_number):
        if show_number:
            headers = ["Number", "Name", "Distance", "Emergency Type", "Danger Level", "Survivor Count", "Required Role"]
            return f"{headers[0]:<10}{headers[1]:<15}{headers[2]:<15}{headers[3]:<20}{headers[4]:<15}{headers[5]:<15}{headers[6]:<15}"
        else:
            headers = ["Name", "Distance", "Emergency Type", "Danger Level", "Survivor Count", "Required Role"]
            return f"{headers[0]:<15}{headers[1]:<15}{headers[2]:<15}{headers[3]:<20}{headers[4]:<15}{headers[5]:<15}"

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


