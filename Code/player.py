import pygame


class Player:
    """Represents the player entity."""

    def __init__(self, settings, start_x, start_y):
        self.settings = settings
        self.size = self.settings.player_size
        self.x = float(start_x)
        self.y = float(start_y)
        self.speed = self.settings.player_speed

    def get_rect(self):
        """Return pygame.Rect representing the player's current integer bounds.

        Uses the player_size attribute from settings.
        """
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def handle_input(self):
        """Return movement vector (dx, dy) based on held keys.

        Uses WASD (controlled by settings.use_wasd) and keeps the original
        behaviour where holding E modifies movement magnitude.
        """
        keys = pygame.key.get_pressed()
        dx = 0.0
        dy = 0.0
        if self.settings.use_wasd:
            if keys[pygame.K_w] and not keys[pygame.K_e]:
                dy -= self.speed
            if keys[pygame.K_s] and not keys[pygame.K_e]:
                dy += self.speed
            if keys[pygame.K_a] and not keys[pygame.K_e]:
                dx -= self.speed
            if keys[pygame.K_d] and not keys[pygame.K_e]:
                dx += self.speed

            if keys[pygame.K_w] and keys[pygame.K_e]:
                dy -= 6 * self.speed
            if keys[pygame.K_s] and keys[pygame.K_e]:
                dy += 6 * self.speed
            if keys[pygame.K_a] and keys[pygame.K_e]:
                dx -= 6 * self.speed
            if keys[pygame.K_d] and keys[pygame.K_e]:
                dx += 6 * self.speed
        return dx, dy

    def update(self, dx, dy):
        """Apply movement immediately. No inertia.

        Updates the player's x and y coordinates.
        """
        self.x += dx
        self.y += dy

    def draw(self, surface, camera_x, camera_y):
        """Draw the player rectangle with camera offset.

        Uses settings.color_player for the player colour.
        """
        rect = (int(self.x - camera_x), int(self.y - camera_y), self.size, self.size)
        pygame.draw.rect(surface, self.settings.color_player, rect)
