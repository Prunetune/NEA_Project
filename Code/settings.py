class Settings:
    """
    Holds all configurable settings for the game.
    """

    def __init__(self):
        """
        Initialize the game's static settings.
        """
        # --- Window Settings (16:9) ---
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60

        # --- Map Generation ---
        self.tile_size = 32
        self.repeat_x = 10
        self.repeat_y = 10
        self.map_width_tiles = 10 * self.repeat_x
        self.map_height_tiles = 7 * self.repeat_y

        # --- Spawns ---
        self.enemy_spawn_count = 15
        self.trap_spawn_count = 10

        # --- HUD (UI) ---
        self.hud_bar_width = 200
        self.hud_bar_height = 20
        self.hud_offset_x = 20
        self.hud_offset_y_hp = 20
        self.hud_offset_y_mana = 50

        # --- Player Stats ---
        self.max_health = 100
        self.player_health = 100
        self.player_speed = 5
        self.player_max_mana = 100
        self.mana_regen = 0.5
        self.spell_cost = 15
        self.player_size = 28
        self.iframe_duration = 1000

        # --- Dash Physics (Smooth) ---
        self.dash_cooldown = 600
        self.dash_force = 25
        self.dash_friction = 0.85

        # --- Projectile Stats ---
        self.projectile_speed = 10
        self.projectile_damage = 25
        self.projectile_lifetime = 1000
        self.projectile_cooldown = 800

        # --- Enemy/Trap Stats ---
        self.enemy_health_default = 50
        self.enemy_damage = 10
        self.trap_damage = 15
        self.enemy_speed = 2.5
        self.enemy_search_dist = 400
        self.enemy_repath_rate = 1200
        self.enemy_node_limit = 40
        self.enemy_map_check_bias = 0.2

        # Knockback Physics
        self.knockback_strength = 15
        self.knockback_friction = 0.85

        # --- Camera ---
        self.camera_margin = 0.20
        self.camera_smoothing = 0.12

        # --- Colors ---
        self.color_bg = (20, 20, 20)
        self.color_floor = (40, 40, 40)
        self.color_wall = (100, 100, 100)
        self.color_player = (0, 200, 0)
        self.color_enemy = (200, 0, 0)
        self.color_projectile = (0, 255, 255)
        self.color_trap = (150, 0, 200)
        self.color_hud_bg = (50, 50, 50)
        self.color_hp = (0, 200, 0)
        self.color_hp_bg = (100, 0, 0)
        self.color_mana = (0, 100, 255)
        self.color_border = (255, 255, 255)