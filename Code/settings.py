class Settings:
    """
    Holds all configurable settings for the game.
    """

    def __init__(self):
        """
        Initialize the game's static settings.
        """
        # --- Window Settings (16:9) --- #
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60

        # --- Map Generation --- #
        self.tile_size = 32
        self.repeat_x = 10
        self.repeat_y = 10
        self.map_width_tiles = 10 * self.repeat_x
        self.map_height_tiles = 7 * self.repeat_y

        # --- Spawns --- #
        self.enemy_spawn_count = 0
        self.archer_spawn_count= 40
        self.trap_spawn_count = 30

        # --- HUD (UI) --- #
        self.hud_bar_width = 200
        self.hud_bar_height = 20
        self.hud_offset_x = 20
        self.hud_offset_y_hp = 20
        self.hud_offset_y_mana = 50

        # --- Player Stats --- #
        self.max_health = 100
        self.player_health = 100
        self.player_speed = 5
        self.player_max_mana = 100
        self.mana_regen = 0.3
        self.water_bullet_spell_cost = 15
        self.player_size = 28
        self.iframe_duration = 1000

        # --- Dash Physics --- #
        self.dash_cooldown = 600
        self.dash_force = 25
        self.dash_friction = 0.85

        # --- Fireball Spell --- #
        self.fireball_spell_cost = 40
        self.fireball_damage = 40
        self.fireball_speed = 12
        self.fireball_height = 16
        self.fireball_width = 16
        self.fireball_aoe_radius = 10
        self.fireball_max_aoe_radius = 100
        self.fireball_trail_length = 10
        self.fireball_alpha = 255

        # --- Lightning Spell --- #
        self.lightning_damage = 20
        self.lightning_range = 10
        self.lightning_cost = 50
        self.lightning_max_jumps = 6
        self.lightning_duration = 35

        # --- Heal Spell ---#
        self.heal_spell_cost = 10
        self.heal_spell_amount = 10
        self.heal_cooldown = 800

        # --- Projectile Stats ---#
        self.projectile_speed = 10
        self.projectile_damage = 25
        self.projectile_lifetime = 1000
        self.projectile_cooldown = 800

        # --- Enemy/Trap Stats ---#
        self.enemy_health = 50
        self.enemy_damage = 10
        self.enemy_speed = 2.5
        self.enemy_search_dist = 600
        self.enemy_repath_rate = 1
        self.enemy_node_limit = 40
        self.enemy_map_check_bias = 0.2

        # --- Archer Stats ---#
        self.archer_health = 30
        self.archer_damage = 5
        self.archer_speed = 10
        self.archer_search_dist = 600
        self.archer_repath_rate = 1
        self.archer_node_limit = 40
        self.archer_map_check_bias = 0.2
        self.archer_attack_cooldown = 700

        # --- Trap Stats --- #
        self.trap_damage = 15

        #  --- Knockback Physics --- #
        self.knockback_strength = 15
        self.knockback_friction = 0.85

        # --- Camera --- #
        self.camera_margin = 0.20
        self.camera_smoothing = 0.12

        # --- Colors --- #
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
        self.color_archer = (71, 99, 30)
        self.color_fireball = (255, 100, 0)
        self.color_explosion = (255, 200, 0)
        self.color_lightning = (150, 230, 255)