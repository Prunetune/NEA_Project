import pygame
from .timer import CooldownTimer
from.enemy import Enemy

class Archer(Enemy):
    def __init__(self, settings, x, y):
        """
        Initialize enemy and AI settings.
        """
        super().__init__(settings,x,y)
        self.settings = settings

        self.image = pygame.Surface((settings.player_size, settings.player_size))
        self.image.fill(settings.color_archer)


        self.health = settings.archer_health
        self.damage = settings.archer_damage

        self.state = "IDLE"
        self.path = []
        self.repath_timer = CooldownTimer(settings.archer_repath_rate)