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


# Display the medic equipment to verify that it was created
print("MEDIC EQUIPMENT")
print("Future assigned ship: Rectafongulus")
print("=" * 50)

#for item in medical_equipment:
   # item.display_info()


