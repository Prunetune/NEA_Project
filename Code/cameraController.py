class CameraController:
    """Manage camera position and smooth following behavior."""

    def __init__(self, settings):
        self.settings = settings
        self.cameraX = 0.0
        self.cameraY = 0.0

    def update(self, player):
        """Adjust cameraX and cameraY so the player stays inside defined margins."""

        #The camera updates separately for X and Y axes and uses linear interpolation
        #to move smoothly toward target offsets.

        sw = self.settings.screenWidth
        sh = self.settings.screenHeight
        marginX = sw * self.settings.cameraMargin
        marginY = sh * self.settings.cameraMargin

        # player position relative to camera
        px_screen = player.x - self.cameraX
        py_screen = player.y - self.cameraY

        targetX = self.cameraX
        targetY = self.cameraY

        if px_screen + player.size > sw - marginX:
            targetX += (px_screen + player.size) - (sw - marginX)
        elif px_screen < marginX:
            targetX -= (marginX - px_screen)

        if py_screen + player.size > sh - marginY:
            targetY += (py_screen + player.size) - (sh - marginY)
        elif py_screen < marginY:
            targetY -= (marginY - py_screen)

        # linear interpolation towards target
        lerp = self.settings.cameraSmoothing
        self.cameraX += (targetX - self.cameraX) * lerp
        self.cameraY += (targetY - self.cameraY) * lerp

    def get_offsets(self):
        """Return integer camera offsets for drawing (cameraX, cameraY)."""
        return int(self.cameraX), int(self.cameraY)
