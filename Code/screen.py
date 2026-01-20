import pygame

class Screen:
    """Create and hold the main Pygame surface."""

    def __init__(self, settings):
        """Initialise Pygame and create the main window surface."""

        self.settings = settings
        pygame.init()
        # Create fixed-size window using settings. Windowed mode as requested.
        self.surface = pygame.display.set_mode((self.settings.screenWidth, self.settings.screenHeight))
        pygame.display.set_caption("Arcana Realms V0.1")

    def get_surface(self):
        """Return the main drawing surface."""
        return self.surface

    def clear(self):
        """Fill background colour."""
        self.surface.fill(self.settings.colorBg)
