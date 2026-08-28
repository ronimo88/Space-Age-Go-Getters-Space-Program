class MedicalEquipment:
    def __init__(self, name, purpose, weight, status="Ready"):
        self.name = name
        self.purpose = purpose
        self.weight = weight
        self.status = status

    def display_info(self):
        print(f"Equipment: {self.name}")
        print(f"Purpose: {self.purpose}")
        print(f"Weight: {self.weight} kg")
        print(f"Status: {self.status}")
        print("-" * 50)


# Create only the medic's equipment
medical_equipment = [
    MedicalEquipment(
        "Human Rescue Hoist",
        "Lifts stranded or injured people to safety",
        250,
    ),
    MedicalEquipment(
        "Zero-Gravity Stretcher",
        "Moves injured people without worsening their injuries",
        45,
    ),
    MedicalEquipment(
        "Emergency Trauma Kit",
        "Treats bleeding, burns, and broken bones",
        20,
    ),
    MedicalEquipment(
        "Portable Oxygen System",
        "Provides oxygen to survivors who cannot breathe normally",
        30,
    ),
    MedicalEquipment(
        "Medical Scanner",
        "Checks vital signs and identifies injuries",
        12,
    ),
    MedicalEquipment(
        "Thermal Rescue Blanket",
        "Protects survivors from extreme temperatures",
        5,
    ),
    MedicalEquipment(
        "Portable Medical Pod",
        "Stabilizes critically injured people during transport",
        300,
    ),
]


# Display the medic equipment to verify that it was created
print("MEDIC EQUIPMENT")
print("Future assigned ship: Rectafongulus")
print("=" * 50)

for item in medical_equipment:
    item.display_info()


