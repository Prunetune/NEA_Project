class Settings:
    """Holds configurable settings for the game."""

    def __init__(self):
        # window size
        self.screen_width = 800
        self.screen_height = 800

        # Tile / map sizes
        self.tile_size = 32                 # each tile is 32x32 pixels
        self.player_size = 28               # player is 28x28 pixels

        # Movement and timing
        self.player_speed = 4               # pixels per frame
        self.fps = 60                       # baseline frames per second
        # the number of frames passed until another dash can be made
        self.dash_cooldown = 180

        # Camera behaviour
        self.camera_margin = 0.20          # 20% of screen: camera starts to follow
        self.camera_smoothing = 0.12       # makes the movement of the camera look smooth

        # Map repetition (4x screen area)
        # builds a small base pattern and repeat it to reach full world size.
        self.repeat_x = 4
        self.repeat_y = 4

        # Colours
        self.color_bg = (20, 20, 20)
        self.color_floor = (40, 40, 40)
        self.color_wall = (100, 100, 100)
        self.color_player = (0, 200, 0)

        # Controls
        self.use_wasd = True               # using WASD for movement

        # Debug / inefficiency flags
        self.bruteforce_draw = True        # draw the entire map every frame (slow when True)
