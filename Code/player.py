import pygame
from settings import Settings

class Player:
    """Represents the player entity."""

    def __init__(self, settings, startX, startY):
        self.settings = settings
        self.size = self.settings.playerSize
        self.x = float(startX)
        self.y = float(startY)
        self.speed = self.settings.playerSpeed

    def get_rect(self):
        """Return pygame.Rect representing the player's current integer bounds."""
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def handle_input(self):
        """Return movement vector (dx, dy) based on held keys. Uses WASD and full-speed diagonals."""
        keys = pygame.key.get_pressed()
        dx = 0.0
        dy = 0.0
        if self.settings.useWASD:
            if keys[pygame.K_w]:
                dy -= self.speed
            if keys[pygame.K_s]:
                dy += self.speed
            if keys[pygame.K_a]:
                dx -= self.speed
            if keys[pygame.K_d]:
                dx += self.speed
        return dx, dy

    def update(self, dx, dy):
        """Apply movement immediately. No inertia."""
        self.x += dx
        self.y += dy

    def draw(self, surface, cameraX, cameraY):
        """Draw the player rectangle with camera offset."""
        rect = (int(self.x - cameraX), int(self.y - cameraY), self.size, self.size)
        pygame.draw.rect(surface, self.settings.colorPlayer, rect)
