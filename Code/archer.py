import pygame
from .timer import CooldownTimer

class Archer(pygame.sprite.Sprite):
    def __init__(self, settings, x, y):
        """
        Initialize enemy and AI settings.
        """
        super().__init__()
        self.settings = settings

        self.image = pygame.Surface((settings.player_size, settings.player_size))
        self.image.fill(settings.color_archer)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos = pygame.Vector2(x, y)
        self.health = settings.enemy_health_default
        self.damage = settings.enemy_damage
        self.last_hit_time = 0

        self.state = "IDLE"
        self.path = []
        self.repath_timer = CooldownTimer(settings.enemy_repath_rate)