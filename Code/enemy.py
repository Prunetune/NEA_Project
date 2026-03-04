import pygame
import math
import random
from .timer import CooldownTimer


class Enemy(pygame.sprite.Sprite):
    """
    Basic enemy entity with pathfinding.
    """

    def __init__(self, settings, x, y):
        """
        Initialize enemy and AI settings.
        """
        super().__init__()
        self.settings = settings

        self.image = pygame.Surface((settings.player_size, settings.player_size))
        self.image.fill(settings.color_enemy)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos = pygame.Vector2(x, y)
        self.health = settings.enemy_health
        self.damage = settings.enemy_damage
        self.last_hit_time = 0

        self.state = "IDLE"
        self.path = []
        self.repath_timer = CooldownTimer(settings.enemy_repath_rate)

    def take_damage(self, amount):
        """
        Reduce health with I-Frames.
        """
        now = pygame.time.get_ticks()

        if now - self.last_hit_time > self.settings.iframe_duration:
            self.health -= amount
            self.last_hit_time = now

            if self.health <= 0:
                self.kill()

    def get_distance_to_target(self, target_pos):
        """
        Calculate distance using vector math.
        """
        return math.sqrt((target_pos.x - self.pos.x) ** 2 + (target_pos.y - self.pos.y) ** 2)

    def calculate_path(self, start, target, tile_map):
        """
        A* algorithm to find the best path to the player.
        """
        open_list = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        nodes_checked = 0

        while open_list and nodes_checked < self.settings.enemy_node_limit:
            nodes_checked += 1
            open_list.sort(key=lambda x: x[0])
            current = open_list.pop(0)[1]

            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)

                if 0 <= neighbor[1] < tile_map.rows and 0 <= neighbor[0] < tile_map.cols:
                    tile_value = tile_map.map_data[neighbor[1]][neighbor[0]]

                    # Logic to verify if the tile is passable
                    if tile_value == 0 or random.random() < self.settings.enemy_map_check_bias:
                        temp_g = g_score[current] + 1
                        if neighbor not in g_score or temp_g < g_score[neighbor]:
                            came_from[neighbor] = current
                            g_score[neighbor] = temp_g
                            f = temp_g + abs(neighbor[0] - target[0]) + abs(neighbor[1] - target[1])
                            open_list.append((f, neighbor))
        return []

    def update(self, collision_machine, player, tile_map,):
        """
        Update position and pathfinding state.
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

        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)


    def draw(self, surface, cam_x, cam_y):
        """
        Draw relative to camera.
        """
        draw_rect = self.rect.copy()
        draw_rect.x -= cam_x
        draw_rect.y -= cam_y
        surface.blit(self.image, draw_rect)