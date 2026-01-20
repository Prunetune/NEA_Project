class CameraController:
    """Manage camera position and smooth following behaviour."""

    def __init__(self, settings):
        self.settings = settings
        self.camera_x = 0.0
        self.camera_y = 0.0

    def update(self, player):
        """Adjust camera_x and camera_y so the player stays inside defined margins."""

        # the camera updates separately for x and y axes and uses linear interpolation
        # to move smoothly toward target offsets

        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        margin_x = screen_width * self.settings.camera_margin
        margin_y = screen_height * self.settings.camera_margin

        # player position relative to the camera
        player_screen_x = player.x - self.camera_x
        player_screen_y = player.y - self.camera_y

        target_x = self.camera_x
        target_y = self.camera_y

        if player_screen_x + player.size > screen_width - margin_x:
            target_x += (player_screen_x + player.size) - (screen_width - margin_x)
        elif player_screen_x < margin_x:
            target_x -= margin_x - player_screen_x

        if player_screen_y + player.size > screen_height - margin_y:
            target_y += (player_screen_y + player.size) - (screen_height - margin_y)
        elif player_screen_y < margin_y:
            target_y -= margin_y - player_screen_y

        # linear interpolation towards the target camera position
        lerp = self.settings.camera_smoothing
        self.camera_x += (target_x - self.camera_x) * lerp
        self.camera_y += (target_y - self.camera_y) * lerp

    def get_offsets(self):
        """Return integer camera offsets for drawing (camera_x, camera_y)."""
        return int(self.camera_x), int(self.camera_y)
