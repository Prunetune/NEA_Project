import pygame

from .projectiles import Projectile
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
        self.speed = settings.archer_speed

        self.attack_cooldown= CooldownTimer(settings.archer_attack_cooldown)

        self.state = "IDLE"
        self.path = []
        self.repath_timer = CooldownTimer(settings.archer_repath_rate)
        self.enemy_id = "Archer"

    def fire_projectiles(self, target):
        if self.attack_cooldown.is_ready():
            #print("test 1") ## Checks to make sure it makes it through first condition,THIS CHECK COMPLETES
            player_position = target
            position = self.pos

            direction = player_position - position
            if 0 < direction.length() <= 100:
                #print("test 2") ## Checks to make sure it makes it through second condition, THIS CHECK COMPLETES
                direction = direction.normalize()
                return Projectile(self.settings, self.pos.x, self.pos.y, direction)
        return None

    def update(self, collision_machine, player, tile_map):
         super().update(collision_machine,player,tile_map)



