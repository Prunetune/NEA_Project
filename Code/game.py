import sys
import pygame
from settings import Settings
from screen import Screen
from tileMap import TileMap
from player import Player
from interactableBlock import InteractableBlock
from cameraController import CameraController
from collisionDetection import CollisionDetection


class Game:
    """Main game controller. Creates instances of all systems and runs the game loop."""

    def __init__(self):
        # create settings and core systems
        self.settings = Settings()
        self.screen = Screen(self.settings)
        self.surface = self.screen.get_surface()
        self.tile_map = TileMap(self.settings)

        # spawn player near world centre
        start_x = (self.tile_map.pixel_width // 2) - (self.settings.player_size // 2)
        start_y = (self.tile_map.pixel_height // 2) - (self.settings.player_size // 2)
        self.player = Player(self.settings, start_x, start_y)

        # create interactable blocks placed around the world
        self.blocks = []
        block_spacing = self.settings.tile_size

        # example positions relative to centre
        self.blocks.append(
            InteractableBlock(start_x + block_spacing * 2, start_y, self.settings.player_size)
        )
        self.blocks.append(
            InteractableBlock(start_x - block_spacing * 3, start_y + block_spacing * 2, self.settings.player_size)
        )

        self.camera = CameraController(self.settings)
        self.collision = CollisionDetection(self.settings)

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        """Main loop. Handles input, updates logic, and draws each frame."""
        while self.running:
            self.handle_events()

            # input -> movement
            dx, dy = self.player.handle_input()

            # apply movement
            self.player.update(dx, dy)

            # collect obstacles: tile walls and active interactable blocks
            obstacles = self.tile_map.get_all_wall_rects()[:]
            for block in self.blocks:
                obstacles.append(block.get_rect())

            # collision resolution (player only)
            self.collision.resolve_collision(self.player, obstacles)

            # update camera after movement and collision
            self.camera.update(self.player)
            cam_x, cam_y = self.camera.get_offsets()

            # draw everything
            self.screen.clear()
            self.tile_map.draw(self.surface, cam_x, cam_y)

            for block in self.blocks:
                block.draw(self.surface, cam_x, cam_y)

            self.player.draw(self.surface, cam_x, cam_y)

            # flip display and cap frame rate
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Process events.
        ESC quits immediately.
        Other events are intentionally minimal for demo scope.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # immediate quit when ESC is pressed
                    self.running = False

                elif event.key == pygame.K_e:
                    # interact with nearest interactable_block when pressing E
                    self.try_interact()

    def try_interact(self):
        """Attempt to interact with any interactable_block the player is overlapping.
        Interaction toggles the block's active state.
        """
        player_rect = self.player.get_rect()

        for block in self.blocks:
            if player_rect.colliderect(block.get_rect()):
                block.on_interact()
