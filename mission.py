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
            Ship("Rectafongulus", 10, 40, 4, 800),
            Ship("Savior", 12, 60, 3.5, 900),
            Ship("Avenger", 15, 80, 3, 1000),
            Ship("Tank", 20, 100, 2.5, 1200)
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
                "Fichina",
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

        self.available_members = [
            CrewMember("Ron", "Commander", 250),
            CrewMember("Sean", "Commander", 200),
            CrewMember("Eric", "Pilot", 180),
            CrewMember("Sunny", "Pilot", 125),
            CrewMember("Anthony", "Engineer", 175),
            CrewMember("Tom", "Engineer", 175),
            CrewMember("Mendell", "Medic", 225),
            CrewMember("John", "Medic", 150),
            CrewMember("Brian", "Mechanic", 275),
            CrewMember("Keyon", "Mechanic", 225)
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

