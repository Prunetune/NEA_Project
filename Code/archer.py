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

    def fire_projectiles(self, target):
        if self.attack_cooldown.is_ready():
            print("test 1") ## Checks to make sure it makes it through first condition
            player_postition= target
            postition = self.pos

            direction = player_postition - postition
            if 0 < direction.length() <= 1000:
                print("test 2") ## Checks to make sure it makes it through second condition
                direction = direction.normalize()
                return Projectile(self.settings, self.pos.x, self.pos.y, direction)
        return None

    def update(self, collision_machine, player, tile_map):
        """
               Update position, pathfinding  and projectile spawning.
               """
        dist = self.get_distance_to_target(pygame.Vector2(player.rect.center))

        if self.state == "IDLE":
            if dist < self.settings.enemy_search_dist:
                self.state = "CHASE"

        elif self.state == "CHASE":
            if dist > self.settings.enemy_search_dist + 100:
                self.state = "IDLE"
                self.path = []

            if not self.path or self.repath_timer.is_ready():
                start_tile = (int(self.rect.centerx // self.settings.tile_size),
                              int(self.rect.centery // self.settings.tile_size))
                target_tile = (int(player.rect.centerx // self.settings.tile_size),
                               int(player.rect.centery // self.settings.tile_size))
                self.path = self.calculate_path(start_tile, target_tile, tile_map)
                self.repath_timer.trigger()

            if self.path:
                node = self.path[0]
                target_px = pygame.Vector2(node[0] * self.settings.tile_size,
                                           node[1] * self.settings.tile_size)

                direction = target_px - self.pos
                if direction.length() > 2:
                    velocity = direction.normalize() * self.settings.enemy_speed
                    self.pos += velocity
                else:
                    self.path.pop(0)

        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        self.fire_projectiles(player.get_position())

        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)