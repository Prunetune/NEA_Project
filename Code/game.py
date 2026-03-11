import sys
import pygame
import random

from .settings import Settings
from .screen import Screen
from .tileMap import TileMap
from .player import Player
from .cameraController import CameraController
from .collisionDetection import CollisionDetection
from .hud import HUD
from .enemy import Enemy
from .trap import Trap
from .archer import Archer



class Game:
    """
    Main Game Controller.
    """

    def __init__(self):
        """
        Initialize systems.
        """
        self.settings = Settings()
        self.screen = Screen(self.settings)
        self.surface = self.screen.get_surface()
        self.hud = HUD(self.settings)

        self.tile_map = TileMap(self.settings)
        self.camera = CameraController(self.settings)
        self.collision = CollisionDetection(self.settings)

        # --- SAFE SPAWN LOGIC ---
        spawn_pos = self.get_safe_spawn_point()
        self.player = Player(self.settings, spawn_pos[0], spawn_pos[1])

        self.enemies = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.populate_world()

        self.clock = pygame.time.Clock()
        self.running = True

    def get_safe_spawn_point(self):
        """
        Finds a coordinate that is NOT a wall.
        """
        while True:
            tx = random.randint(1, self.settings.map_width_tiles - 2)
            ty = random.randint(1, self.settings.map_height_tiles - 2)

            if self.tile_map.map_data[ty][tx] == 0:
                return tx * self.settings.tile_size, ty * self.settings.tile_size

    def populate_world(self):
        """
        Spawns entities in safe spots.
        """
        for i in range(self.settings.enemy_spawn_count):
            pos = self.get_safe_spawn_point()
            self.enemies.add(Enemy(self.settings, pos[0], pos[1]))

        for i in range(self.settings.archer_spawn_count):
            pos = self.get_safe_spawn_point()
            self.enemies.add(Archer(self.settings, pos[0], pos[1]))

        for i in range(self.settings.trap_spawn_count):
            pos = self.get_safe_spawn_point()
            self.traps.add(Trap(self.settings, pos[0], pos[1]))




    def run(self):
        """
        Main Loop.
        """
        while self.running:
            self.handle_events()

            # --- DEATH CHECK ---
            if self.player.health <= 0:
                print("Game Over!")
                self.running = False

            cam_x, cam_y = self.camera.get_offsets()
            view_rect = self.camera.get_view_rect()

            new_projectile = self.player.handle_input(cam_x, cam_y)

            if new_projectile:
                self.projectiles.add(new_projectile)



            # 1. Physics & Wall Collision
            nearby_walls = self.tile_map.get_nearby_walls(self.player.rect)
            self.player.update(self.collision, nearby_walls)

            # 2. Enemy Collision (Knockback)
            self.collision.resolve_enemy_collision(self.player, self.enemies)

            self.camera.update(self.player)

            visible_enemies = [e for e in self.enemies if view_rect.colliderect(e.rect)]
            visible_traps = [t for t in self.traps if view_rect.colliderect(t.rect)]

            for i in visible_enemies:
                i.update(self.collision, self.player, self.tile_map)

            for i in visible_traps:
                i.update(self.collision, self.player)

            for i in visible_enemies:
                if i.get_enemy_id() == "Archer":
                    temp = i.fire_projectiles(self.player.pos)
                    if temp is not None:
                        self.projectiles.add(temp)




            # FIX: Pass self.tile_map so projectiles check their OWN nearby walls
            self.projectiles.update(self.collision, self.tile_map, self.enemies, self.player)

            self.screen.clear()
            self.tile_map.draw(self.surface, cam_x, cam_y)

            for i in visible_traps:
                i.draw(self.surface, cam_x, cam_y)

            for i in visible_enemies:
                i.draw(self.surface, cam_x, cam_y)

            for i in self.projectiles:
                i.draw(self.surface, cam_x, cam_y)

            self.player.draw(self.surface, cam_x, cam_y)
            self.hud.draw(self.surface, self.player)

            pygame.display.flip()
            self.clock.tick(self.settings.fps)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                self.running = False

            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                self.running = False