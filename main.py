import sys
import pygame
print("Target Package:", pygame.__file__)
print("Version Info:", pygame.version.ver)
import random

from mission import Mission

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("audio/music.mp3")
# Set volume (0.0 to 1.0)
pygame.mixer.music.set_volume(1)

WIDTH, HEIGHT = 1200, 760
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Age Go-Getters Space Program")
CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 20)
SMALL = pygame.font.SysFont("consolas", 16)
TITLE = pygame.font.SysFont("consolas", 34, bold=True)
BIG = pygame.font.SysFont("consolas", 48, bold=True)
HUGE = pygame.font.SysFont("consolas", 100, bold=True)

SPLASH_BG = (0, 0, 0)
BG = (7, 12, 25)
PANEL = (15, 24, 43)
PANEL_2 = (20, 32, 55)
TEXT = (225, 235, 250)
MUTED = (145, 165, 195)
BLUE = (70, 160, 255)
GREEN = (80, 220, 130)
RED = (245, 90, 100)
YELLOW = (245, 205, 80)
WHITE = (255, 255, 255)

DANGER_COLORS = {
    1: GREEN,
    2: YELLOW,
    3: (255, 165, 75),
    4: (255, 110, 80),
    5: RED,
}

ROLE_COLORS = {
    "Commander": (170, 130, 255),
    "Engineer": (80, 190, 255),
    "Medic": (90, 220, 150),
    "Mechanic": (255, 170, 80),
    "Pilot": (240, 120, 220),
}

EQUIPMENT_COLORS = {
    "Human Rescue Hoist": (170, 130, 255),
    "Emergency Trauma Kit": (80, 190, 255),
    "Thermal Rescue Blanket": (90, 220, 150),
    "Medical Scanner": (255, 170, 80),
}

TAB_WIDTH = 220

STARS = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 2)) for _ in range(150)]

LAUNCH_SOUND = pygame.mixer.Sound("audio/launch.mp3")
SUCCESS_SOUND = pygame.mixer.Sound("audio/mission_complete.mp3")
INTRO_SOUND = pygame.mixer.Sound("audio/intro.mp3")
CRAWL_TITLE = "SPACE AGE GO-GETTERS"

try:
    TITLE_SURFACE = pygame.image.load('images/title_text.png').convert_alpha()
except pygame.error as e:
    print(f"Unable to load image: {e}")
    sys.exit()

CRAWL_TEXT = [
    "It is a perilous time for the galaxy.",
    "",
    "Distress signals echo across the stars from",
    "crews stranded on hostile worlds, their ships",
    "crippled and supplies running low.",
    "",
    "You command the last rescue fleet capable of",
    "reaching them in time. Choose your ship wisely,",
    "assemble a crew fit for the danger ahead, and",
    "gather the equipment needed to bring everyone",
    "home safely.",
    "",
    "The mission begins now....",
]


def text(surface, value, font, color, x, y):
    surface.blit(font.render(str(value), True, color), (x, y))


def center(surface, value, font, color, position):
    image = font.render(str(value), True, color)
    surface.blit(image, image.get_rect(center=position))


def panel(surface, rect, title=None):
    pygame.draw.rect(surface, PANEL, rect, border_radius=12)
    pygame.draw.rect(surface, (45, 65, 95), rect, 2, border_radius=12)
    if title:
        text(surface, title, FONT, BLUE, rect.x + 18, rect.y + 14)

def draw_starfield():
    SCREEN.fill((0, 0, 0))
    for x, y, size in STARS:
        pygame.draw.circle(SCREEN, WHITE, (x, y), size)


class Button:
    def __init__(self, rect, label, callback, enabled=True):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.callback = callback
        self.enabled = enabled

    def draw(self, surface):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())

        if not self.enabled:
            fill, border, color = (40, 48, 62), (60, 70, 85), (105, 115, 130)
        elif hovered:
            fill, border, color = (35, 70, 110), BLUE, WHITE
        else:
            fill, border, color = PANEL_2, (65, 90, 125), TEXT

        pygame.draw.rect(surface, fill, self.rect, border_radius=8)
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=8)
        center(surface, self.label, SMALL, color, self.rect.center)

    def handle(self, event):
        if (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.callback()
            return True
        return False


class Game:
    # Pages requested by the user.
    PAGES = ["RESCUE SITE", "SHIP", "CREW", "EQUIPMENT", "MISSION"]

    def __init__(self):
        self.page = None
        self.reset()
        self.muted = False
        self.start_delay = 45
        self.crawl_y = HEIGHT + 500  # start below the screen
        self.crawl_speed = 0.6  # px per frame, tune to taste
        self.crawl_started = False
        self.crawl_done = False
        self.title_font_size = 200
        self.title_width = TITLE_SURFACE.get_width()
        self.title_height = TITLE_SURFACE.get_height()
        self.splash = True  # NEW — show splash on startup
        self.splash_start = pygame.time.get_ticks()
        INTRO_SOUND.play()
        INTRO_SOUND.set_volume(1)

    def reset(self):
        self.mission = Mission()
        self.page = "RESCUE SITE"
        self.message = "Select a rescue site to begin planning."
        self.message_color = TEXT
        self.result = None
        self.launch_start = 0
        self.launching = False
        self.mission_running = True
        self.credits_y = HEIGHT
        self.credits_timer = 0
        self.mission_success = False
        SUCCESS_SOUND.stop()

    def go_to_credits(self):
        self.page = "CREDITS"
        self.set_message("")

    @property
    def site(self):
        return self.mission.selected_rescue_site

    @property
    def ship(self):
        return self.mission.selected_ship

    def draw_crawl(self):
        draw_starfield()

        # Title card fades in at the very start

        if self.crawl_y > HEIGHT + 200:
            #title_font = pygame.font.SysFont("consolas", int(self.title_font_size), bold=True)
            #center(SCREEN, CRAWL_TITLE, title_font, YELLOW, (WIDTH // 2, HEIGHT // 2 - 50))

            # Resize using the calculated dimensions
            resized_image = pygame.transform.scale(TITLE_SURFACE, (self.title_width, self.title_height))
            new_rect = resized_image.get_rect()
            new_rect.center = (WIDTH // 2, HEIGHT // 2)
            SCREEN.blit(resized_image, new_rect)


        line_height = 34
        y = self.crawl_y

        if self.title_width > 1:
            self.title_width -= 3

        if self.title_height > 1:
            self.title_height -= 1

        for line in reversed(CRAWL_TEXT):  # <-- only change
            depth = max(0.0, min(1.0, (HEIGHT * 0.9 - y) / (HEIGHT * 0.9)))
            scale = max(0.35, 1.0 - depth * 0.65)

            if line and -40 < y < HEIGHT:
                font_size = max(10, int(30 * scale))
                crawl_font = pygame.font.SysFont("consolas", font_size, bold=True)
                rendered = crawl_font.render(line, True, YELLOW)
                rect = rendered.get_rect(center=(WIDTH // 2, int(y)))
                SCREEN.blit(rendered, rect)

            y -= line_height * scale

        self.crawl_y -= self.crawl_speed
        self.title_font_size -= 0.5

        # End the crawl once everything has scrolled off the top
        if y < -50:
            self.crawl_done = True
            INTRO_SOUND.stop()

    def draw_splash(self):
        SCREEN.fill(SPLASH_BG)

        center(SCREEN, "SPACE AGE GO-GETTERS ", BIG, WHITE, (WIDTH // 2, 280))
        center(SCREEN, "SPACE PROGRAM", TITLE, BLUE, (WIDTH // 2, 340))

        # simple pulsing "press to continue" prompt
        elapsed = pygame.time.get_ticks() - self.splash_start
        if (elapsed // 500) % 2 == 0:  # blinks every 0.5s
            center(SCREEN, "Click or press any key to begin", FONT, MUTED, (WIDTH // 2, 460))

    def set_message(self, message, color=TEXT):
        self.message = message
        self.message_color = color

    def select_site(self, site):
        self.mission.selected_rescue_site = site
        self.set_message(f"Rescue site selected: {site.name}", GREEN)

    def select_ship(self, ship):
        self.mission.selected_ship = ship
        self.set_message(f"Ship selected: {ship.name}", GREEN)

    def add_member(self, member):
        self.mission.crew_members.append(member)
        self.mission.available_members.remove(member)
        self.set_message(f"{member.name} added to the crew.", GREEN)

    def remove_member(self, member):
        self.mission.available_members.append(member)
        self.mission.crew_members.remove(member)
        self.set_message(f"{member.name} removed from the crew.", YELLOW)

    def add_equipment(self, item):
        self.mission.selected_equipment.append(item)
        self.mission.available_equipment.remove(item)
        self.set_message(f"{item.name} added to the equipment list.", GREEN)

    def remove_equipment(self, item):
        self.mission.available_equipment.append(item)
        self.mission.selected_equipment.remove(item)
        self.set_message(f"{item.name} removed from the equipment list.", YELLOW)

    def toggle_mute(self):
        self.muted = not self.muted

        if self.muted:
            pygame.mixer.music.set_volume(0)
            self.set_message("Sound muted.", YELLOW)
        else:
            pygame.mixer.music.set_volume(1.0)
            self.set_message("Sound unmuted.", GREEN)

    def draw_mute_button(self):
        rect = pygame.Rect(WIDTH - 130, 10, 120, 40)

        hovered = rect.collidepoint(pygame.mouse.get_pos())

        if hovered:
            fill = (35, 70, 110)
            border = BLUE
        else:
            fill = PANEL
            border = (65, 90, 125)

        pygame.draw.rect(
            SCREEN,
            fill,
            rect,
            border_radius=8
        )

        pygame.draw.rect(
            SCREEN,
            border,
            rect,
            2,
            border_radius=8
        )

        label = "UNMUTE" if self.muted else "MUTE"

        center(
            SCREEN,
            label,
            SMALL,
            WHITE,
            rect.center
        )

    def evaluate_mission(self):
        if not self.site:
            return False, "No rescue site selected.", RED

        if not self.ship:
            return False, "No ship selected.", RED

        remaining = self.ship.capacity - len(self.mission.crew_members)
        if remaining < self.site.survivor_count:
            return (
                False,
                "There is not enough room for the survivors.",
                RED,
            )

        if not any(
            member.role == "Pilot"
            for member in self.mission.crew_members
        ):
            return (
                False,
                f"You don't have a pilot to fly the ship.",
                RED,
            )

        if not any(
            member.role == self.site.required_role
            for member in self.mission.crew_members
        ):
            return (
                False,
                f"{self.site.name} requires a {self.site.required_role}.",
                RED,
            )

        if not any(
            item.name == self.site.required_equipment
            for item in self.mission.selected_equipment
        ):
            return (
                False,
                f"{self.site.name} requires a {self.site.required_equipment}.",
                RED,
            )

        if self.mission.travel_hours > self.mission.selected_rescue_site.rescue_time:
            return (
                False,
                f"It took too long to reach {self.site.name}. All the survivors died.",
                RED,
            )

        return (
            True,
            f"Everyone has been rescued from {self.site.name}!",
            GREEN,
        )

    def launch(self):
        success, message, color = self.evaluate_mission()
        self.result = (success, message, color)
        self.launching = True
        self.launch_start = pygame.time.get_ticks()
        pygame.mixer.music.stop()
        LAUNCH_SOUND.play()

    def go_to(self, page):
        self.page = page
        self.set_message(f"{page.title()} page")

    def handle_event(self, event):

        if not self.crawl_done:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.crawl_done = True
                INTRO_SOUND.stop()
            return

        if self.splash:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.splash = False
                pygame.mixer.music.play(-1)
            return  # ignore all other input while splash is up

        if self.page == "CREDITS":
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                pygame.mixer.music.play(-1)
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.go_to("RESCUE SITE")
            elif event.key == pygame.K_2:
                self.go_to("SHIP")
            elif event.key == pygame.K_3:
                self.go_to("CREW")
            elif event.key == pygame.K_4:
                self.go_to("EQUIPMENT")
            elif event.key == pygame.K_5:
                self.go_to("MISSION")
            elif event.key == pygame.K_ESCAPE and self.launching:
                self.launching = False
                self.result = None
                self.page = "MISSION"
                pygame.mixer.music.play(-1)

        # Mute Button
        mute_rect = pygame.Rect(WIDTH - 130, 10, 120, 40)

        if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and mute_rect.collidepoint(event.pos)
        ):
            self.toggle_mute()
            return


        if self.launching:
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and pygame.Rect(WIDTH // 2 - 120, 535, 240, 50).collidepoint(event.pos)
            ):
                if self.mission_success:
                    self.launching = False
                    self.go_to_credits()
                else:
                    self.reset()
                    pygame.mixer.music.play(-1)

            return

        # Navigation tabs.
        for i, page in enumerate(self.PAGES):
            rect = pygame.Rect(30 + i * (TAB_WIDTH+10), 92, TAB_WIDTH, 48)
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and rect.collidepoint(event.pos)
            ):
                self.go_to(page)
                return

        if self.page == "RESCUE SITE":
            for i, site in enumerate(self.mission.rescue_sites):
                rect = pygame.Rect(50, 225 + i * 110, 1100, 90)
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and rect.collidepoint(event.pos)
                ):
                    self.select_site(site)

        elif self.page == "SHIP":
            for i, ship in enumerate(self.mission.ships):
                rect = pygame.Rect(50, 225 + i * 130, 1100, 105)
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and rect.collidepoint(event.pos)
                ):
                    self.select_ship(ship)

        elif self.page == "CREW":
            # Available crew on left.
            for i, member in enumerate(self.mission.available_members):
                rect = pygame.Rect(50, 240 + i * 48, 500, 38)
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and rect.collidepoint(event.pos)
                ):
                    self.add_member(member)
                    return

            # Current crew on right.
            for i, member in enumerate(self.mission.crew_members):
                rect = pygame.Rect(650, 240 + i * 48, 500, 38)
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and rect.collidepoint(event.pos)
                ):
                    self.remove_member(member)
                    return

        elif self.page == "EQUIPMENT":
            # Available equipment on left.
            for i, member in enumerate(self.mission.available_equipment):
                rect = pygame.Rect(50, 240 + i * 48, 500, 38)
                if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1
                        and rect.collidepoint(event.pos)
                ):
                    self.add_equipment(member)
                    return

            # Current crew on right.
            for i, item in enumerate(self.mission.selected_equipment):
                rect = pygame.Rect(650, 240 + i * 48, 500, 38)
                if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1
                        and rect.collidepoint(event.pos)
                ):
                    self.remove_equipment(item)
                    return

        elif self.page == "MISSION":
            launch_rect = pygame.Rect(300, 650, 340, 55)
            reset_rect = pygame.Rect(60, 650, 170, 55)

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and launch_rect.collidepoint(event.pos)
            ):
                self.launch()
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and reset_rect.collidepoint(event.pos)
            ):
                self.reset()

    def draw_header(self):
        text(SCREEN, "SPACE AGE GO-GETTERS", TITLE, TEXT, 30, 22)
        text(SCREEN, "RESCUE MISSION CONTROL", SMALL, MUTED, 32, 62)
        pygame.draw.line(SCREEN, (45, 65, 95), (30, 82), (1170, 82), 2)

        for i, page in enumerate(self.PAGES):
            rect = pygame.Rect(30 + i * (TAB_WIDTH + 10), 92, TAB_WIDTH, 48)
            active = page == self.page
            fill = (30, 65, 100) if active else PANEL
            border = BLUE if active else (55, 75, 105)

            pygame.draw.rect(SCREEN, fill, rect, border_radius=8)
            pygame.draw.rect(SCREEN, border, rect, 2, border_radius=8)
            center(SCREEN, f"{i + 1}. {page}", SMALL, WHITE if active else MUTED, rect.center)

    def site_positions(self):
        # A schematic game map. Positions are intentionally arranged
        # for gameplay and are not intended to represent real astronomy.
        return {
            "Corneria": (205, 350),
            "Fichina": (470, 550),
            "Titania": (745, 350),
            "Venom": (1000, 550),
        }

    def draw_space_map(self):
        panel(SCREEN, pygame.Rect(30, 175, 1140, 550), "GALACTIC RESCUE MAP")

        text(
            SCREEN,
            "Click a destination to select it.",
            SMALL,
            MUTED,
            50,
            150,
        )

        positions = self.site_positions()

        # Space field
        map_rect = pygame.Rect(50, 225, 1100, 475)
        pygame.draw.rect(SCREEN, (5, 10, 22), map_rect, border_radius=10)
        pygame.draw.rect(SCREEN, (45, 65, 95), map_rect, 2, border_radius=10)

        # Decorative stars
        for i in range(95):
            x = map_rect.x + ((i * 97 + 41) % (map_rect.width - 10)) + 5
            y = map_rect.y + ((i * 53 + 17) % (map_rect.height - 10)) + 5
            radius = 1 if i % 5 else 2
            pygame.draw.circle(SCREEN, (100, 120, 155), (x, y), radius)

        # Draw schematic routes between destinations.
        sites = self.mission.rescue_sites
        for i in range(len(sites) - 1):
            a = positions[sites[i].name]
            b = positions[sites[i + 1].name]
            pygame.draw.line(SCREEN, (45, 65, 95), a, b, 2)

        # Home/base station.
        base_pos = (600, 450)
        pygame.draw.circle(SCREEN, (75, 160, 255), base_pos, 34)
        pygame.draw.circle(SCREEN, (210, 235, 255), base_pos, 24)
        pygame.draw.circle(SCREEN, (75, 160, 255), base_pos, 15)
        center(SCREEN, "BASE", SMALL, WHITE, (base_pos[0], base_pos[1] + 52))

        # Draw destinations.
        mouse = pygame.mouse.get_pos()

        for site in sites:
            x, y = positions[site.name]
            selected = site is self.site
            hovered = pygame.Rect(x - 45, y - 45, 90, 90).collidepoint(mouse)

            danger_color = DANGER_COLORS.get(site.danger_level, MUTED)
            radius = 31 if selected else 25

            if selected:
                pygame.draw.circle(SCREEN, BLUE, (x, y), radius + 10, 3)

            if hovered:
                pygame.draw.circle(SCREEN, WHITE, (x, y), radius + 6, 2)

            # Planet appearance varies by danger level.
            pygame.draw.circle(SCREEN, danger_color, (x, y), radius)
            pygame.draw.circle(SCREEN, (10, 18, 35), (x - 8, y - 6), max(4, radius // 5))
            pygame.draw.circle(SCREEN, (10, 18, 35), (x + 10, y + 9), max(3, radius // 6))

            # Planet label and mission data.
            center(SCREEN, site.name, SMALL, WHITE, (x, y - 53))
            center(
                SCREEN,
                f"{site.distance} LY",
                SMALL,
                MUTED,
                (x, y + 50),
            )

            # Selection hotspot.
            hotspot = pygame.Rect(x - 48, y - 48, 96, 96)
            if (
                pygame.mouse.get_pressed()[0]
                and hotspot.collidepoint(mouse)
            ):
                self.select_site(site)

        # Legend
        legend_x = 75
        legend_y = 660


        # Selected destination details.
        if self.site:
            text(
                SCREEN,
                f"Selected: {self.site.name}",
                SMALL,
                GREEN,
                legend_x,
                legend_y-80,
            )
            text(
                SCREEN,
                f"Survivors: {self.site.survivor_count}",
                SMALL,
                MUTED,
                legend_x,
                legend_y-60,
            )
            text(
                SCREEN,
                f"Required Role: {self.site.required_role}",
                SMALL,
                MUTED,
                legend_x,
                legend_y-40,
            )
            text(
                SCREEN,
                f"Required Equipment: {self.site.required_equipment}",
                SMALL,
                MUTED,
                legend_x,
                legend_y-20,
            )
            text(
                SCREEN,
                f"Rescue Time Limit: {self.site.rescue_time} hours",
                SMALL,
                MUTED,
                legend_x,
                legend_y,
            )

    def draw_ship(self):
        panel(SCREEN, pygame.Rect(30, 175, 1140, 550), "SHIP SELECTION")

        text(
            SCREEN,
            "Choose the rescue vessel that will carry your crew and survivors.",
            SMALL,
            MUTED,
            50,
            150,
        )

        for i, ship in enumerate(self.mission.ships):
            y = 225 + i * 120
            rect = pygame.Rect(50, y, 1100, 105)
            selected = ship is self.ship

            pygame.draw.rect(
                SCREEN,
                (25, 48, 75) if selected else PANEL_2,
                rect,
                border_radius=8,
            )
            pygame.draw.rect(
                SCREEN,
                BLUE if selected else (55, 75, 105),
                rect,
                2,
                border_radius=8,
            )

            text(SCREEN, ship.name, FONT, WHITE, 75, y + 15)
            text(SCREEN, f"Capacity: {ship.capacity}", SMALL, MUTED, 75, y + 55)
            text(SCREEN, f"Fuel: {ship.fuel:,} gallons", SMALL, MUTED, 300, y + 55)
            text(SCREEN, f"Speed: {ship.speed:,} LY/hr", SMALL, MUTED, 600, y + 55)

            if selected:
                text(SCREEN, "SELECTED", SMALL, GREEN, 980, y + 15)


    def draw_crew(self):
        panel(SCREEN, pygame.Rect(30, 175, 1140, 550), "CREW MANAGEMENT")

        text(
            SCREEN,
            "Add and remove crew members. Check the rescue site to see what roles are needed.",
            SMALL,
            MUTED,
            50,
            150,
        )

        text(SCREEN, "Available crew", FONT, BLUE, 50, 215)
        text(SCREEN, "Crew aboard", FONT, GREEN, 650, 215)

        for i, member in enumerate(self.mission.available_members):
            y = 240 + i * 48
            rect = pygame.Rect(50, y, 500, 38)

            pygame.draw.rect(SCREEN, PANEL_2, rect, border_radius=6)
            pygame.draw.rect(SCREEN, (55, 75, 105), rect, 1, border_radius=6)

            text(
                SCREEN,
                f"+ {member.name}",
                SMALL,
                ROLE_COLORS.get(member.role, TEXT),
                65,
                y + 8,
            )
            text(SCREEN, member.role, SMALL, MUTED, 245, y + 8)
            text(SCREEN, f"{member.weight} lbs", SMALL, MUTED, 405, y + 8)

        for i, member in enumerate(self.mission.crew_members):
            y = 240 + i * 48
            rect = pygame.Rect(650, y, 500, 38)

            pygame.draw.rect(SCREEN, (30, 55, 42), rect, border_radius=6)
            pygame.draw.rect(SCREEN, GREEN, rect, 1, border_radius=6)

            text(
                SCREEN,
                f"- {member.name}",
                SMALL,
                ROLE_COLORS.get(member.role, TEXT),
                665,
                y + 8,
            )
            text(SCREEN, member.role, SMALL, MUTED, 845, y + 8)
            text(SCREEN, "CLICK TO REMOVE", SMALL, MUTED, 965, y + 8)

        if not self.mission.crew_members:
            text(SCREEN, "No crew selected.", SMALL, MUTED, 650, 240)

    def draw_equipment(self):
        panel(SCREEN, pygame.Rect(30, 175, 1140, 550), "EQUIPMENT MANAGEMENT")

        text(
            SCREEN,
            "Add and remove crew equipment. Check the rescue site to see what equipment is needed.",
            SMALL,
            MUTED,
            50,
            150,
        )

        text(SCREEN, "Available equipment", FONT, BLUE, 50, 215)
        text(SCREEN, "Equipment aboard", FONT, GREEN, 650, 215)

        for i, item in enumerate(self.mission.available_equipment):
            y = 240 + i * 48
            rect = pygame.Rect(50, y, 500, 38)

            pygame.draw.rect(SCREEN, PANEL_2, rect, border_radius=6)
            pygame.draw.rect(SCREEN, (55, 75, 105), rect, 1, border_radius=6)

            text(
                SCREEN,
                f"+ {item.name}",
                SMALL,
                EQUIPMENT_COLORS.get(item.name, TEXT),
                65,
                y + 8,
            )

            text(SCREEN, f"{item.weight} lbs", SMALL, MUTED, 405, y + 8)

        for i, item in enumerate(self.mission.selected_equipment):
            y = 240 + i * 48
            rect = pygame.Rect(650, y, 500, 38)

            pygame.draw.rect(SCREEN, (30, 55, 42), rect, border_radius=6)
            pygame.draw.rect(SCREEN, GREEN, rect, 1, border_radius=6)

            text(
                SCREEN,
                f"- {item.name}",
                SMALL,
                EQUIPMENT_COLORS.get(item.name, TEXT),
                665,
                y + 8,
            )

            text(SCREEN, "CLICK TO REMOVE", SMALL, MUTED, 965, y + 8)

        if not self.mission.selected_equipment:
            text(SCREEN, "No equipment selected.", SMALL, MUTED, 650, 240)

    def draw_mission(self):
        panel(SCREEN, pygame.Rect(30, 175, 1140, 550), "MISSION REVIEW")

        # The Launch datetime picker

        text(
            SCREEN,
            "Review mission information and launch the mission when you are ready!",
            SMALL,
            MUTED,
            50,
            150,
        )

        text(SCREEN, "Mission information", FONT, BLUE, 50, 225)

        if self.site:
            text(SCREEN, f"Rescue Site: {self.site.name}", SMALL, TEXT, 70, 260)
            text(
                SCREEN,
                f"Survivors: {self.site.survivor_count}",
                SMALL,
                MUTED,
                70,
                275,
            )
            text(
                SCREEN,
                f"Required Role: {self.site.required_role}",
                SMALL,
                ROLE_COLORS.get(self.site.required_role, TEXT),
                70,
                310,
            )
            text(
                SCREEN,
                f"Required Equipment: {self.site.required_equipment}",
                SMALL,
                EQUIPMENT_COLORS.get(self.site.required_equipment, TEXT),
                70,
                345,
            )
            text(
                SCREEN,
                f"Rescue Time Limit: {self.site.rescue_time}",
                SMALL,
                MUTED,
                70,
                380,
            )
        else:
            text(SCREEN, "No rescue site selected.", SMALL, RED, 70, 260)

        if self.ship:
            text(SCREEN, f"Ship: {self.ship.name}", SMALL, TEXT, 70, 475)
            text(
                SCREEN,
                f"Capacity: {self.ship.capacity}",
                SMALL,
                MUTED,
                70,
                510,
            )
            text(
                SCREEN,
                f"Speed: {self.ship.speed} LY/hr",
                SMALL,
                MUTED,
                70,
                545,
            )
            remaining = self.ship.capacity - len(self.mission.crew_members)
            text(
                SCREEN,
                f"Remaining seats: {remaining}",
                SMALL,
                GREEN if remaining >= (self.site.survivor_count if self.site else 0) else RED,
                70,
                580,
            )

        else:
            text(SCREEN, "No ship selected.", SMALL, RED, 70, 475)

        text(
            SCREEN,
            f"Crew members aboard: {len(self.mission.crew_members)}",
            SMALL,
            TEXT,
            600,
            260,
        )

        if self.site:
            has_role = any(
                member.role == self.site.required_role
                for member in self.mission.crew_members
            )
            has_equipment = any(
                item.name == self.site.required_equipment
                for item in self.mission.selected_equipment
            )
            text(
                SCREEN,
                f"Required-role check: {'READY' if has_role else 'MISSING'}",
                SMALL,
                GREEN if has_role else RED,
                600,
                295,
            )
            text(
                SCREEN,
                f"Required-equipment check: {'READY' if has_equipment else 'MISSING'}",
                SMALL,
                GREEN if has_equipment else RED,
                600,
                330,
            )

        Button(
            (60, 650, 170, 55),
            "RESET",
            self.reset,
        ).draw(SCREEN)

        launch_ready = self.site is not None and self.ship is not None
        Button(
            (300, 650, 340, 55),
            "LAUNCH MISSION",
            self.launch,
            launch_ready,
        ).draw(SCREEN)

    def draw_launch_date(self):
        # Launch time
        if self.site and self.ship:
            launch_time, arrival_time, travel_hours = self.mission.calculate_mission_time()
            self.mission.travel_hours = travel_hours

            text(
                SCREEN,
                f"Launch Time: {launch_time.strftime('%m/%d/%Y %I:%M %p')}",
                SMALL,
                MUTED,
                600,
                475
            )

            text(
                SCREEN,
                f"Estimated Arrival Time: {arrival_time.strftime('%m/%d/%Y %I:%M %p')}",
                SMALL,
                MUTED,
                600,
                505
            )

            if travel_hours <= self.mission.selected_rescue_site.rescue_time:
                color = GREEN
                message = f"Travel Time: {travel_hours:.2f} hours: READY"
            else:
                color = RED
                message = f"Travel Time: {travel_hours:.2f} hours: NOT READY"

            text(
                SCREEN,
                message,
                SMALL,
                color,
                600,
                535
            )

    def draw_launch(self):
        elapsed = pygame.time.get_ticks() - self.launch_start

        if (
            self.mission.selected_rescue_site is None or
            self.mission.selected_ship is None or
            not any(
                member.role == "Pilot"
                for member in self.mission.crew_members
            )
        ):
            progress = 1
        else:
            progress = min(1.0, elapsed / 4000.0)

        for i in range(80):
            x = (i * 83 + 37) % WIDTH
            y = (i * 47 + 113) % HEIGHT
            pygame.draw.circle(SCREEN, (100, 120, 150), (x, y), 1)

        if progress < 1:

            center(SCREEN, "MISSION LAUNCH", BIG, WHITE, (WIDTH // 2, 100))

            sx = int(500 + 200 * progress)
            sy = 600 - int(500 * progress)

            pygame.draw.polygon(
                SCREEN,
                WHITE,
                [
                    (sx, sy),
                    (sx - 60, sy + 25),
                    (sx - 35, sy + 25),
                    (sx - 55, sy + 55),
                    (sx, sy + 40),
                    (sx + 55, sy + 55),
                    (sx + 35, sy + 25),
                    (sx + 60, sy + 25),
                ],
            )
            pygame.draw.circle(SCREEN, BLUE, (sx, sy + 25), 8)

            return

        LAUNCH_SOUND.stop()

        success, message, color = self.result

        if success and self.mission_running:
            SUCCESS_SOUND.play()
            self.mission_running = False
            self.mission_success = True


        center(
            SCREEN,
            "MISSION SUCCESS" if success else "MISSION FAILED",
            BIG,
            color,
            (WIDTH // 2, 325),
        )
        center(SCREEN, message, FONT, TEXT, (WIDTH // 2, 400))

        if self.site:
            center(
                SCREEN,
                f"Destination: {self.site.name} | Survivors: {self.site.survivor_count}",
                SMALL,
                MUTED,
                (WIDTH // 2, 450),
            )

        if self.ship:
            center(
                SCREEN,
                f"Ship: {self.ship.name} | Crew aboard: {len(self.mission.crew_members)}",
                SMALL,
                MUTED,
                (WIDTH // 2, 480),
            )

        if success:
            Button(
                (WIDTH // 2 - 120, 535, 240, 50),
                "CONTINUE",
                self.go_to_credits,
            ).draw(SCREEN)
        else:
            Button(
                (WIDTH // 2 - 120, 535, 240, 50),
                "PLAY AGAIN",
                self.reset,
            ).draw(SCREEN)


    def draw_credits(self):
        SCREEN.fill(SPLASH_BG)

        names = [
            "TEAM LEAD",
            "Ron Morrison",
            "",
            "TEAM MEMBERS",
            "Anthony Ortega",
            "Brian Goin",
            "Mendell Jackson",
            "Eric Uzoukwu",
            "",
            "THANKS FOR PLAYING!"
        ]

        x = WIDTH // 2
        y = self.credits_y

        for name in names:
            center(
                SCREEN,
                name,
                TITLE,
                MUTED,
                (x, y)
            )

            y += 50

        self.credits_y -= 1
        self.credits_timer += 1

        if self.credits_timer > 15*60:
            self.reset()
            pygame.mixer.music.play(-1)

    def draw(self):

        if self.start_delay <= 0 and not self.crawl_started:
            self.crawl_started = True
        else:
            self.start_delay -= 1

        if not self.crawl_started:
            return

        if not self.crawl_done:
            self.draw_crawl()
            return

        if self.splash:
            self.draw_splash()
            return

        SCREEN.fill(BG)

        if not self.launching and self.page != "CREDITS":
            self.draw_header()

        if self.launching:
            self.draw_launch()
        elif self.page == "RESCUE SITE":
            self.draw_space_map()
        elif self.page == "SHIP":
            self.draw_ship()
        elif self.page == "CREW":
            self.draw_crew()
        elif self.page == "EQUIPMENT":
            self.draw_equipment()
        elif self.page == "MISSION":
            self.draw_mission()
            self.draw_launch_date()
        elif self.page == "CREDITS":
            self.draw_credits()

        if not self.launching and self.message:
            text(SCREEN, self.message, SMALL, self.message_color, 30, 735)

        self.draw_mute_button()

        # Mute Button


def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game.handle_event(event)

        game.draw()
        pygame.display.flip()
        CLOCK.tick(60)


if __name__ == "__main__":
    main()
