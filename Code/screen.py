import pygame

class Screen:
    """
    Manages the OS window and main drawing surface.
    """

    def __init__(self, settings):
        """
        Initialize Pygame video system.
        """
        self.settings = settings
        pygame.init()
        self.surface = pygame.display.set_mode((settings.screen_width, settings.screen_height))
        pygame.display.set_caption("Arcana Realms")

    def get_surface(self):
        """
        Return the main drawing surface.
        """
        return self.surface

    def clear(self):
        """
        Wipe the screen clean.
        """
        self.surface.fill(self.settings.color_bg)