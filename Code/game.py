
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
    """Main game controller. Creates instances of all systems and runs the loop."""

    def __init__(self):
        # create settings and systems
        self.settings = Settings()
        self.screenObj = Screen(self.settings)
        self.surface = self.screenObj.get_surface()
        self.tileMap = TileMap(self.settings)

        # spawn player near world centre
        startX = (self.tileMap.pixelWidth // 2) - (self.settings.playerSize // 2)
        startY = (self.tileMap.pixelHeight // 2) - (self.settings.playerSize // 2)
        self.player = Player(self.settings, startX, startY)

        # create a few interactable blocks placed around the world
        self.blocks = []
        bs = self.settings.tileSize
        # example positions relative to centre
        self.blocks.append(InteractableBlock(startX + bs*2, startY, self.settings.playerSize))
        self.blocks.append(InteractableBlock(startX - bs*3, startY + bs*2, self.settings.playerSize))

        self.camera = CameraController(self.settings)
        self.collision = CollisionDetection(self.settings)

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        """Main loop. Handles input, updates logic, draws each frame."""
        while self.running:
            self.handle_events()

            # input -> movement
            dx, dy = self.player.handle_input()
            # apply movement
            self.player.update(dx, dy)

            # collect obstacles: walls and active blocks
            obstacles = self.tileMap.get_all_wall_rects()[:]
            for b in self.blocks:
                obstacles.append(b.get_rect())

            # collision check and resolution (player only for now)
            self.collision.resolve_collision(self.player, obstacles)

            # camera update after movement/collision to keep player away from edges
            self.camera.update(self.player)
            camX, camY = self.camera.get_offsets()

            # draw everything (brute-force draw intentionally)
            self.screenObj.clear()
            self.tileMap.draw(self.surface, camX, camY)
            for b in self.blocks:
                b.draw(self.surface, camX, camY)
            self.player.draw(self.surface, camX, camY)

            # flip and cap framerate
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Process events. ESC quits immediately.
           Other events are intentionally minimal to match the demo scope.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # immediate quit when ESC is pressed
                    self.running = False
                elif event.key == pygame.K_e:
                    # example: interact with nearest block when pressing E
                    self.try_interact()

    def try_interact(self):
        """Attempt to interact with any block the player is overlapping.
           Interaction is simple: toggle the block's active state.
        """
        prect = self.player.get_rect()
        for b in self.blocks:
            if prect.colliderect(b.get_rect()):
                b.on_interact()
