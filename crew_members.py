
class CrewMember:
    def __init__(self, name, role, weight):
        self.name = name
        self.role = role # Medic, Engineer, Pilot, Commander
        self.weight = weight # In Kilograms

    def summary(self):
        return (
            f"{self.name:<15}{self.role:<15}{self.weight:<15}"
        )

    def update_role(self, new_role):
        self.role = new_role

    def update_weight(self, new_weight):
        self.weight = new_weight





