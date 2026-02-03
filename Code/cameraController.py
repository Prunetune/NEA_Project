import pygame


class CameraController:
    """
    Manages the 'Camera' viewport.
    """

    def __init__(self, settings):
        """
        Start the camera at 0,0.
        """
        self.settings = settings
        self.camera_x = 0.0
        self.camera_y = 0.0

    def update(self, player):
        """
        Follow player and clamp to map bounds.
        """
        target_x = player.x - self.settings.screen_width / 2
        target_y = player.y - self.settings.screen_height / 2

        # Smooth movement
        self.camera_x += (target_x - self.camera_x) * self.settings.camera_smoothing
        self.camera_y += (target_y - self.camera_y) * self.settings.camera_smoothing

        # Clamping
        map_pixel_width = self.settings.map_width_tiles * self.settings.tile_size
        map_pixel_height = self.settings.map_height_tiles * self.settings.tile_size

        self.camera_x = max(0, int(min(self.camera_x, map_pixel_width - self.settings.screen_width)))
        self.camera_y = max(0, int(min(self.camera_y, map_pixel_height - self.settings.screen_height)))

    def get_offsets(self):
        """
        Returns integer camera coordinates.
        """
        return int(self.camera_x), int(self.camera_y)

    def get_view_rect(self):
        """
        Returns the camera's view rectangle.
        """
        return pygame.Rect(self.camera_x, self.camera_y,
                           self.settings.screen_width, self.settings.screen_height)