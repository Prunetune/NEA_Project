import pygame
from .timer import CooldownTimer
from .projectiles import Projectile


class Player(pygame.sprite.Sprite):
    """
    Main player character.
    """

    def __init__(self, settings, x, y):
        """
        Initialize player.
        """
        super().__init__()
        self.settings = settings
        self.size = settings.player_size

        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(settings.color_player)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.x = float(x)
        self.y = float(y)

        # Movement Vectors
        self.vel_x = 0
        self.vel_y = 0
        self.knockback = pygame.Vector2(0, 0)  # New knockback vector

        self.health = settings.max_health
        self.mana = settings.player_max_mana

        self.dash_timer = CooldownTimer(settings.dash_cooldown)
        self.shoot_timer = CooldownTimer(settings.projectile_cooldown)

        self.is_dashing = False
        self.dash_start = 0
        self.last_hit_time = 0

    def handle_input(self, cam_x, cam_y):
        """
        Handle Keys (WASD) and Mouse.
        """
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        self.vel_y = 0
        speed = self.settings.player_speed

        # --- WASD MOVEMENT ---
        # Disable input movement if being knocked back hard
        if self.knockback.length() < 2:
            if keys[pygame.K_a]:
                self.vel_x = -speed

            if keys[pygame.K_d]:
                self.vel_x = speed

            if keys[pygame.K_w]:
                self.vel_y = -speed

            if keys[pygame.K_s]:
                self.vel_y = speed

        # --- DASH (Shift) ---
        if keys[pygame.K_LSHIFT] and self.dash_timer.is_ready() and not self.is_dashing:
            if self.vel_x != 0 or self.vel_y != 0:
                self.is_dashing = True
                self.dash_start = pygame.time.get_ticks()
                self.dash_timer.trigger()

        # Dash Physics
        if self.is_dashing:
            if pygame.time.get_ticks() - self.dash_start < self.settings.dash_duration:
                self.vel_x *= 2.5
                self.vel_y *= 2.5
            else:
                self.is_dashing = False

        # --- SHOOT (Left Click) ---
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0] and self.mana >= self.settings.spell_cost and self.shoot_timer.is_ready():
            self.shoot_timer.trigger()
            return self.create_projectile(cam_x, cam_y)

        return None

    def create_projectile(self, cam_x, cam_y):
        """
        Creates a projectile aimed at mouse.
        """
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        world_mouse = mouse_pos + pygame.Vector2(cam_x, cam_y)
        player_center = pygame.Vector2(self.rect.center)

        direction = (world_mouse - player_center)
        if direction.length() > 0:
            direction = direction.normalize()
            self.mana -= self.settings.spell_cost
            return Projectile(self.settings, player_center.x, player_center.y, direction)

        return None

    def apply_knockback(self, direction_vector):
        """
        Add impulse force to player.
        """
        # Only apply if not invincible (prevents stun lock)
        now = pygame.time.get_ticks()
        if now - self.last_hit_time < self.settings.iframe_duration:
            # Still apply force, just no damage (handled in collision),
            # but we want the push!
            self.knockback = direction_vector * self.settings.knockback_strength

    def take_damage(self, amount):
        """
        Lose health with I-Frames.
        """
        now = pygame.time.get_ticks()

        if now - self.last_hit_time > self.settings.iframe_duration:
            self.health -= amount
            self.last_hit_time = now

            if self.health < 0:
                self.health = 0

    def update(self, collision_machine, walls):
        """
        Physics and Updates.
        """
        # Mana Regen
        if self.mana < self.settings.player_max_mana:
            self.mana += self.settings.mana_regen

        # --- COMBINE FORCES ---
        # Add knockback velocity to input velocity
        self.vel_x += self.knockback.x
        self.vel_y += self.knockback.y

        # Apply Friction to Knockback (Decay)
        self.knockback *= self.settings.knockback_friction

        # Stop micro-sliding
        if self.knockback.length() < 0.5:
            self.knockback = pygame.Vector2(0, 0)

        # 1. Resolve Wall Collisions (Now uses Sub-Stepping)
        collision_machine.resolve_wall_collision(self, walls)

        # 2. Map Clamping
        map_w = self.settings.map_width_tiles * self.settings.tile_size
        map_h = self.settings.map_height_tiles * self.settings.tile_size

        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0

        if self.x > map_w - self.size:
            self.x = map_w - self.size

        if self.y > map_h - self.size:
            self.y = map_h - self.size

        # 3. Sync Rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, surface, cam_x, cam_y):
        """
        Draw relative to camera.
        """
        draw_rect = self.rect.copy()
        draw_rect.x -= cam_x
        draw_rect.y -= cam_y

        # Flash effect for I-Frames
        if pygame.time.get_ticks() - self.last_hit_time < self.settings.iframe_duration:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                pygame.draw.rect(surface, (255, 255, 255), draw_rect)
                return

        pygame.draw.rect(surface, self.settings.color_player, draw_rect)