import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, settings, x, y):
        super().__init__()
        self.settings = settings
        self.pos = pygame.Vector2(x, y)
        self.radius = settings.fireball_aoe_radius
        self.max_radius = settings.fireball_max_aoe_radius
        self.alpha = settings.fireball_alpha
        self.rect = pygame.Rect(x, y, 1, 1)  # Needed for group compatibility
        self.id = "Explosion"
    def update(self, *args):
        """Expands and fades out."""
        self.radius += 6
        self.alpha -= 15
        if self.radius >= self.max_radius or self.alpha <= 0:
            self.kill()

    def draw(self, surface, cam_x, cam_y):
        # Create a surface for transparency
        size = self.radius * 2
        temp_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        color = (*self.settings.color_explosion, max(0, self.alpha))

        pygame.draw.circle(temp_surf, color, (self.radius, self.radius), self.radius, 4)
        surface.blit(temp_surf, (self.pos.x - self.radius - cam_x, self.pos.y - self.radius - cam_y))