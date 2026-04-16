import pygame
import random
from .explosion import Explosion


class Fireball(pygame.sprite.Sprite):
    def __init__(self, settings, x, y, direction):
        super().__init__()
        self.settings = settings
        self.image = pygame.Surface((settings.fireball_height,settings.fireball_width), pygame.SRCALPHA)
        pygame.draw.circle(self.image, settings.colour_fireball, (8, 8), 8)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)
        self.vel = direction * settings.fireball_speed
        self.trail = []  # Stores [x, y, radius]
        self.id = "Fireball"

    def update(self, collision_machine, tile_map, enemies , player):
        # Simple Trail Effect
        self.trail.append([self.pos.x, self.pos.y, 8])
        if len(self.trail) > self.settings.fireball_trail_length: # if the list of points where the fireball has
            self.trail.pop(0)                                     # exceeded 10 it clears the oldest value

        # Movement
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Collision Logic
        hit_wall = False
        for wall in tile_map.get_nearby_walls(self.rect): # checks if the fireball hit a wall
            if self.rect.colliderect(wall):
                hit_wall = True

        if hit_wall or collision_machine.check_projectile_hit(self, enemies): # checks for collision with both enemies
            self.explode(enemies)                                              # and wall collision

    def explode(self, enemies):
        """Deals AoE damage and spawns the visual effect."""
        for enemy in enemies: # checks the current list of enemies
            enemy_pos = pygame.Vector2(enemy.rect.center)
            if self.pos.distance_to(enemy_pos) <= self.settings.fireball_max_aoe_radius: # finds out if the enemies are
                enemy.take_damage(self.settings.fireball_damage)                         # within the range of fireball
                                                                                         # radius
        # Add visual explosion to the same group as the fireball
        explosion = Explosion(self.settings, self.pos.x, self.pos.y)

        for group in self.groups():
            group.add(explosion)
        self.kill()


    def draw(self, surface, cam_x, cam_y):
        if self.trail:
            for i, p in enumerate(self.trail): # i keeps track of index, p loops through every point in self.trail
                rad = int(p[2] * (i / len(self.trail))) # calculates the radius of the current trail circle
                pygame.draw.circle(surface, self.settings.colour_fireball, (int(p[0] - cam_x), int(p[1] - cam_y)),  # draws a solid red circle
                                   rad)





        draw_rect = self.rect.copy() # draws the main body of the fireball
        draw_rect.x -= cam_x
        draw_rect.y -= cam_y
        surface.blit(self.image, draw_rect)