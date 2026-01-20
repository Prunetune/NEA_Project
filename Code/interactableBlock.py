import pygame


class InteractableBlock:
    """Represents a block that can be interacted with and collides like a wall."""


    def __init__(self, x, y, size, color=(180, 100, 50)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        self.active = True # placeholder for interact state


    def get_rect(self):
        return self.rect


    def draw(self, surface, cameraX, cameraY):
        draw_rect = pygame.Rect(int(self.x - cameraX), int(self.y - cameraY), self.size, self.size)
        pygame.draw.rect(surface, self.color, draw_rect)


    def on_interact(self):
        self.active = not self.active