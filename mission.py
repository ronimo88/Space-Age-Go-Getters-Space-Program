from crew_members import CrewMember
from ship import Ship
from rescue_site import RescueSite
from medical_equipment import MedicalEquipment

# Color constants
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

class Mission:
    def __init__(self):
        self.ships = [
            Ship("Rectafongulus", 10, 100, 20000),
            Ship("Savior", 15, 200000, 30000),
            Ship("Avenger", 20, 200000, 30000)
        ]

        self.rescue_sites = [
            RescueSite("Corneria", 10, "", 1, 10, "Medic"),
            RescueSite("Fichina", 20, "", 2, 15, "Engineer"),
            RescueSite("Titania", 20, "", 3, 5, "Commander"),
            RescueSite("Venom", 50, "", 5, 12, "Mechanic")
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
            CrewMember("Anthony", "Engineer", 175),
            CrewMember("Tom", "Engineer", 175),
            CrewMember("Mendell", "Medic", 225),
            CrewMember("John", "Medic", 150),
            CrewMember("Brian", "Mechanic", 275),
            CrewMember("Bob", "Mechanic", 225),
            CrewMember("Eric", "Pilot", 180),
            CrewMember("Sarah", "Pilot", 125)
        ]

        self.selected_ship = None
        self.selected_rescue_site = None
        self.selected_equipment = []
        self.crew_members = []

    def select_rescue_site(self):

        print(f"{BLUE}Select a rescue site{RESET}\n")

        # Prints a summary for each rescue site
        print(RescueSite.get_headers(True))
        for index, site in enumerate(self.rescue_sites):
            print(f"{(index + 1):<10}{site.summary()}")

        print()
        # Loops until a valid user input
        while True:
            try:
                # Users selects a rescue site
                user_input = int(input(f"{BLUE}Enter the corresponding rescue site number: {RESET}"))

                if 1 <= user_input <= len(self.rescue_sites):
                    self.selected_rescue_site = self.rescue_sites[int(user_input) - 1]
                    break
                else:
                    print(f"{RED}Invalid input\n{RESET}")
            except ValueError:
                print(f"{RED}Invalid input\n{RESET}")


    def select_ship(self):
        print(f"{BLUE}Select a ship:\n{RESET}")

        # Prints a summary for each ship
        print(Ship.get_headers(True))
        for index, ship in enumerate(self.ships):
            print(f"{(index + 1):<10}{ship.summary()}")

        print()

        # Loops until a valid user input
        while True:
            try:
                # Users selects a ship
                user_input = int(input(f"{BLUE}Enter the corresponding rescue ship number: {RESET}"))

                if 1 <= user_input <= len(self.ships):
                    self.selected_ship = self.ships[int(user_input) - 1]
                    break
                else:
                    print(f"{RED}Invalid input\n{RESET}")
            except ValueError:
                print(f"{RED}Invalid input\n{RESET}")


    def add_crew_member(self):

        if len(self.available_members) == 0:
            print(f"{RED}No available members to add{RESET}\n")

        else:
            print(f"{BLUE}Select a crew member to add\n{RESET}")

            # Prints a summary for each available members
            headers = ["Number", "Name", "Role", "Weight(lbs)"]
            print(f"{headers[0]:<10}{headers[1]:<15}{headers[2]:<15}{headers[3]:<15}")
            for index, member in enumerate(self.available_members):
                print(f"{(index + 1):<10}{member.summary()}")

            print()

            # Loops until a valid user input
            while True:
                try:
                    # Users selects a ship
                    user_input = int(input(f"{BLUE}Enter the corresponding member number: {RESET}"))

                    if 1 <= user_input <= len(self.available_members):
                        member = self.available_members[int(user_input) - 1]
                        self.crew_members.append(member)
                        self.available_members.remove(member)
                        break
                    else:
                        print(f"{RED}Invalid input\n{RESET}")
                except ValueError:
                    print(f"{RED}Invalid input\n{RESET}")


    def remove_crew_member(self):

        if len(self.crew_members) == 0:
            print(f"{RED}No crew members to remove{RESET}\n")

        else:
            print(f"{BLUE}Select a crew member to remove\n{RESET}")

            # Prints a summary for each available members
            print(Ship.get_headers(True))
            for index, member in enumerate(self.crew_members):
                print(f"{(index + 1):<10}{member.summary()}")

            print()
            # Loops until a valid user input
            while True:
                try:
                    # Users selects a ship
                    user_input = int(input(f"{BLUE}Enter the corresponding member number: {RESET}"))

                    if 1 <= user_input <= len(self.crew_members):
                        member = self.crew_members[int(user_input) - 1]
                        self.available_members.append(member)
                        self.crew_members.remove(member)
                        break
                    else:
                        print(f"{RED}Invalid input\n{RESET}")
                except ValueError:
                    print(f"{RED}Invalid input\n{RESET}")


    def crew_member_summary(self):


        # If no crew members have been added, let the user know
        if len(self.crew_members) == 0:
            print(f"{RED}No crew members have been added.{RESET}")
        else:
            print(f"{BLUE}List of crew members:{RESET}")

            # Prints all the crew members that have been added
            print(CrewMember.get_headers())
            for index, member in enumerate(self.crew_members):
                print(f"{(index + 1):<10}{member.summary()}")


    def check_mission_success(self):

        if not self.selected_rescue_site:
            print(f"{RED}Mission Failed! You didn't choose a site to go to. I guess everyone just wants to stay home.{RESET}\n")

        elif not self.selected_ship:
            print(f"{RED}Mission Failed! You don't have a ship to launch{RESET}\n")

        elif self.selected_ship.capacity - len(self.crew_members) < self.selected_rescue_site.survivor_count:
            print(f"{RED}Mission Failed! You don't have enough room for the survivors{RESET}\n")

        elif not any(member.role == self.selected_rescue_site.required_role for member in self.crew_members):
            print(f"{RED}Mission Failed! You don't have the required role for {self.selected_rescue_site.name}{RESET}\n")

        else:
            print(f"{GREEN}Mission Success! You have rescued everyone from {self.selected_rescue_site.name}!{RESET}\n")
