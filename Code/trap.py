import pygame


class Trap(pygame.sprite.Sprite):
    """
    Static hazard.
    """

    def __init__(self, settings, x, y):
        """
        Initialize trap.
        """
        super().__init__()
        self.settings = settings

        self.image = pygame.Surface((settings.tile_size, settings.tile_size))
        self.image.fill(settings.color_trap)  # GREEN
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = settings.trap_damage

    def update(self, collision_machine, player):
        """
        Check collision with player.
        """
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

    def draw(self, surface, cam_x, cam_y):
        """
        Draw relative to camera.
        """
        draw_rect = self.rect.copy()
        draw_rect.x -= cam_x
        draw_rect.y -= cam_y
        surface.blit(self.image, draw_rect)