import pygame
from .player import Player

class Screen:
    """Create and hold the main Pygame surface."""

    def __init__(self, settings):
        """Initialise Pygame and create the main window surface.

        Uses settings.screen_width and settings.screen_height for the window size.
        """
        self.settings = settings

        pygame.init()
        # Create fixed-size window using settings.screen_width and settings.screen_height
        self.surface = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Arcana Realms V0.1")

        # Create a health bar

        pygame.draw.rect(self.surface,"red",(250,250,300,40))
        pygame.draw.rect(self.surface,"green",(250,250,300 *  Player.get_health_ratio(), 40))

    def get_surface(self):
        """Return the main drawing surface."""
        return self.surface

    def clear(self):
        """Fill the background colour using settings.color_bg."""
        self.surface.fill(self.settings.color_bg)

