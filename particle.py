import pygame
import random
import sys

# Colors
BLACK = (10, 11, 20)
WHITE = (255, 255, 255)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Velocity: slight horizontal spread, fast downward movement
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(4, 8)
        # Life management (how long the particle lasts)
        self.max_life = random.randint(20, 40)
        self.life = self.max_life
        self.initial_radius = random.randint(6, 12)
        self.radius = self.initial_radius

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

        # Shrink over time
        life_ratio = max(0, self.life / self.max_life)
        self.radius = max(1, int(self.initial_radius * life_ratio))

    def get_color(self):
        # Transition: White -> Yellow -> Orange -> Red -> Gray -> Fade
        life_ratio = self.life / self.max_life
        if life_ratio > 0.8:
            return (255, 255, 255)  # Hottest core
        elif life_ratio > 0.6:
            return (255, 255, 100)  # Bright yellow
        elif life_ratio > 0.4:
            return (255, 140, 0)  # Orange
        elif life_ratio > 0.15:
            return (230, 50, 10)  # Deep red
        else:
            # Smoke phase
            smoke_val = int(100 * (life_ratio / 0.15))
            return (smoke_val, smoke_val, smoke_val)

    def draw(self, surface):
        if self.life > 0:
            # Blend colors additively for a glowing effect
            pygame.draw.circle(surface, self.get_color(), (int(self.x), int(self.y)), self.radius)


