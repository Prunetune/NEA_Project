import pygame
import random
from .explosion import Explosion


class Fireball(pygame.sprite.Sprite):
    def __init__(self, settings, x, y, direction):
        super().__init__()
        self.settings = settings
        self.image = pygame.Surface((settings.fireball_height,settings.fireball_width), pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.color_fireball, (8, 8), 8)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)
        self.vel = direction * settings.fireball_speed
        self.trail = []  # Stores [x, y, radius]

    def update(self, collision_machine, tile_map, enemies , player):
        # 1. Simple Trail Effect
        self.trail.append([self.pos.x, self.pos.y, 8])
        if len(self.trail) > self.settings.fireball_trail_length:
            self.trail.pop(0)

        # 2. Movement
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # 3. Collision Logic
        hit_wall = False
        for wall in tile_map.get_nearby_walls(self.rect):
            if self.rect.colliderect(wall):
                hit_wall = True

        if hit_wall or collision_machine.check_projectile_hit(self, enemies):
            self.explode(enemies)

    def explode(self, enemies):
        """Deals AoE damage and spawns the visual effect."""
        for enemy in enemies:
            enemy_pos = pygame.Vector2(enemy.rect.center)
            if self.pos.distance_to(enemy_pos) <= self.settings.fireball_max_aoe_radius:
                enemy.take_damage(self.settings.fireball_damage)


        # Add visual explosion to the same group as the fireball
        explosion = Explosion(self.settings, self.pos.x, self.pos.y)
        for group in self.groups():
            group.add(explosion)
        self.kill()

    def draw(self, surface, cam_x, cam_y):
        # Draw Trail
        for i, p in enumerate(self.trail):
            rad = int(p[2] * (i / len(self.trail)))
            pygame.draw.circle(surface, self.settings.color_fireball, (int(p[0] - cam_x), int(p[1] - cam_y)), rad)

        # Draw Fireball Core
        draw_rect = self.rect.copy()
        draw_rect.x -= cam_x
        draw_rect.y -= cam_y
        surface.blit(self.image, draw_rect)