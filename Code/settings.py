class Settings:
    """Holds configurable settings for the game."""

    def __init__(self):
        self.screenWidth = 800
        self.screenHeight = 800

        # Tile / map sizes
        self.tileSize = 32                 # each tile is 32x32 pixels
        self.playerSize = 28               # player is 28x28 pixels

        # Movement and timing
        self.playerSpeed = 4               # pixels per frame
        self.fps = 60                      # baseline frames per second

        # Camera behaviour
        self.cameraMargin = 0.20           # 20% of screen: camera starts to follow
        self.cameraSmoothing = 0.12        # makes the movement of the camera look smooth

        # Map repetition (4x screen area)
        #builds a small base pattern and repeat it to reach full world size.
        self.repeatX = 4
        self.repeatY = 4

        # Colours
        self.colorBg = (20, 20, 20)
        self.colorFloor = (40, 40, 40)
        self.colorWall = (100, 100, 100)
        self.colorPlayer = (0, 200, 0)

        # Controls
        self.useWASD = True                # using WASD for movement

        # Debug / inefficiency flags
        self.bruteforceDraw = True         # draw the entire map every frame  ( this is really bad as long as this is true remember you need to change it)

