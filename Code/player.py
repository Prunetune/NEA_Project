import pygame
from .Timer import CooldownTimer

class Player:
    """Represents the player entity."""

    def __init__(self, settings, start_x, start_y):
        self.settings = settings
        self.size = self.settings.player_size
        self.x = float(start_x)
        self.y = float(start_y)
        self.speed = self.settings.player_speed

        ##Dash settings

        # Cooldown timer (dash can only be used when ready)
        self.dash_cooldown = CooldownTimer(500)  # 500 ms cooldown

        # Dash speed multiplier
        self.dash_speed = 3

        # How long the dash lasts (milliseconds)
        self.dash_duration_ms = 180

        # Dash state tracking
        self.is_dashing = False
        self.dash_start_time = 0

    def get_rect(self):
        """Return pygame.Rect representing the player's current integer bounds.

        Uses the player_size attribute from settings.
        """
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def handle_input(self):
        """Handle keyboard input and return movement deltas."""

        keys = pygame.key.get_pressed()
        dx = dy = 0

        # ---------------- NORMAL MOVEMENT ----------------
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed

        # ---------------- DASH START ----------------
        # Dash triggers only if:
        # 1. Shift is pressed
        # 2. Player is not already dashing
        # 3. Dash cooldown is ready
        if keys[pygame.K_e] and not self.is_dashing and self.dash_cooldown.is_ready():
            self.is_dashing = True
            self.dash_start_time = pygame.time.get_ticks()
            self.dash_cooldown.trigger()

        # ---------------- DASH EFFECT ----------------
        if self.is_dashing:
            time_elapsed = pygame.time.get_ticks() - self.dash_start_time

            if time_elapsed < self.dash_duration_ms:
                # Multiply movement while dashing
                dx *= self.dash_speed
                dy *= self.dash_speed
            else:
                # Dash finished
                self.is_dashing = False

        return dx, dy

    def update(self, dx, dy):
        """Apply movement to the player."""

        self.x += dx
        self.y += dy

    def draw(self, surface, camera_x, camera_y):
        """Draw the player rectangle with camera offset.

        Uses settings.color_player for the player colour.
        """
        rect = (int(self.x - camera_x), int(self.y - camera_y), self.size, self.size)
        pygame.draw.rect(surface, self.settings.color_player, rect)
