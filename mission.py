from crew_members import CrewMember
from ship import Ship
from rescue_site import RescueSite
from medical_equipment import MedicalEquipment
from datetime import datetime, timedelta

# Color constants
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

class Mission:

    def __init__(self):
        self.launch_time = None

        self.ships = [
            Ship("Savior", 12, 40, 4, 1100),
            Ship("Avenger", 14, 60, 3.5, 1200),
            Ship("Vanguard", 18, 80, 3, 1300),
            Ship("Rectafongulus", 22, 100, 2.5, 1400)
        ]

        self.rescue_sites = [
            RescueSite(
                "Corneria",
                10, 3,
                1,
                10,
                "Medic",
                "Human Rescue Hoist"
            ),
            RescueSite(
                "Katina",
                20,
                8, 2,
                15,
                "Engineer",
                "Emergency Trauma Kit"),
            RescueSite(
                "Titania",
                35,
                10,
                3,
                7,
                "Commander",
                "Thermal Rescue Blanket"
            ),
            RescueSite(
                "Venom",
                50,
                17,
                5,
                12,
                "Mechanic",
                "Medical Scanner"
            )
        ]

        # Create only the medic's equipment
        self.available_equipment = [
            MedicalEquipment(
                "Human Rescue Hoist",
                "Lifts stranded or injured people to safety",
                150,
                5
            ),
            MedicalEquipment(
                "Zero-Gravity Stretcher",
                "Moves injured people without worsening their injuries",
                45,
                5
            ),
            MedicalEquipment(
                "Emergency Trauma Kit",
                "Treats bleeding, burns, and broken bones",
                20,
                5
            ),
            MedicalEquipment(
                "Portable Oxygen System",
                "Provides oxygen to survivors who cannot breathe normally",
                30,
                5
            ),
            MedicalEquipment(
                "Medical Scanner",
                "Checks vital signs and identifies injuries",
                12,
                5
            ),
            MedicalEquipment(
                "Thermal Rescue Blanket",
                "Protects survivors from extreme temperatures",
                5,
                5
            ),
            MedicalEquipment(
                "Portable Medical Pod",
                "Stabilizes critically injured people during transport",
                300,
                5
            ),
        ]

        self.available_members = [
            CrewMember("Ron", "Commander", 250, 10),
            CrewMember("Sean", "Commander", 200, 10),
            CrewMember("Eric", "Pilot", 180, 10),
            CrewMember("Sunny", "Pilot", 125, 10),
            CrewMember("Anthony", "Engineer", 175, 10),
            CrewMember("Tom", "Engineer", 175, 10),
            CrewMember("Mendell", "Medic", 225, 10),
            CrewMember("John", "Medic", 150, 10),
            CrewMember("Brian", "Mechanic", 275, 10),
            CrewMember("Keyon", "Mechanic", 225, 10)
        ]

        self.selected_ship = None
        self.selected_rescue_site = None
        self.selected_equipment = []
        self.crew_members = []
        self.travel_hours = 0

    # Mission time calculation
    def calculate_mission_time(self):
        if self.launch_time is None:
            self.launch_time = datetime.now()

        travel_hours = (
                self.selected_rescue_site.distance /
                self.selected_ship.speed
        )

        arrival_time = (
                self.launch_time +
                timedelta(hours=travel_hours)
        )

        return self.launch_time, arrival_time, travel_hours

    def get_chance(self):
        return 10 * len(self.crew_members) + 5 * len(self.selected_equipment)


