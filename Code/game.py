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
        self.traps = pygame.sprite.Group() # creates a sprite grouping for my traps
        self.projectiles = pygame.sprite.Group()

        self.populate_world()

        self.clock = pygame.time.Clock()
        self.running = True

    def get_safe_spawn_point(self):
        """
        Finds a coordinate that is NOT a wall.
        """
        while True:
            x_spawn = random.randint(1, self.settings.map_width_tiles - 2)
            y_spawn = random.randint(1, self.settings.map_height_tiles - 2)

            if self.tile_map.map_data[y_spawn][x_spawn] == 0:
                return x_spawn * self.settings.tile_size, y_spawn * self.settings.tile_size

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
            pos=self.get_safe_spawn_point() # generates a safe spawn point
            self.traps.add(Trap(self.settings, pos[0], pos[1])) #adds the sprite object to a list so i can update and draw
                                                                 # all at once




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



            #Physics & Wall Collision
            nearby_walls = self.tile_map.get_nearby_walls(self.player.rect)
            self.player.update(self.collision, nearby_walls)

            #Enemy Collision (Knockback)
            self.collision.resolve_enemy_collision(self.player, self.enemies)

            self.camera.update(self.player)

            # find out which traps are actually on camera
            visible_traps = []

            for trap in self.traps:
                if view_rect.colliderect(trap.rect):
                    visible_traps.append(trap)

            for trap in visible_traps:
                trap.update(self.collision, self.player)



            visible_enemies = []

            # Filter enemies by whats visible
            for enemy in self.enemies:
                if view_rect.colliderect(enemy.rect):
                    visible_enemies.append(enemy)


            for enemy in visible_enemies:
                enemy.update(self.collision, self.player, self.tile_map)




            for i in self.projectiles:
                if i.id == "Summon":
                    print("This is being selected to be updated")
                    self.enemies.add(i.spawn_ally())
                    i.summon_update()
                else:
                    i.update(self.collision, self.tile_map, self.enemies, self.player)


            self.screen.clear()
            self.tile_map.draw(self.surface, cam_x, cam_y)

            for trap in visible_traps:
                # We pass the camera offsets so they draw in the right place relative to the player
                trap.draw(self.surface, cam_x, cam_y)

            for i in visible_enemies:
                i.draw(self.surface, cam_x, cam_y)

            for i in self.projectiles:
                if i.id == "Lightning":
                    i.draw(self.surface,cam_x, cam_y , self.player)
                else:
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

    def get_tile_map(self):
        return self.tile_map