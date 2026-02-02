import pygame


class InteractableBlock:
    """Represents a block that can be interacted with and collides like a wall."""

    def __init__(self, x, y, size, color=(180, 100, 50)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

        # rect used for collision detection
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)

        # active state toggled by on_interact
        self.active = True

    def get_rect(self):
        """Return the pygame.Rect representing this interactable_block."""
        return self.rect

    def draw(self, surface, camera_x, camera_y):
        """Draw the interactable_block using camera offsets."""
        draw_rect = pygame.Rect(
            int(self.x - camera_x),
            int(self.y - camera_y),
            self.size,
            self.size)
        pygame.draw.rect(surface, self.color, draw_rect)

    def on_interact(self):
        """Toggle the active state of the interactable_block."""
        self.active = not self.active
