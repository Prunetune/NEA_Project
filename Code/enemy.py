import pygame


class Enemy(pygame.sprite.Sprite):
    """
    Basic enemy entity.
    """

    def __init__(self, settings, x, y):
        """
        Initialize enemy.
        """
        super().__init__()
        self.settings = settings

        self.image = pygame.Surface((settings.player_size, settings.player_size))
        self.image.fill(settings.color_enemy)  # RED
        self.rect = self.image.get_rect(topleft=(x, y))

        self.health = settings.enemy_health_default
        self.damage = settings.enemy_damage
        self.last_hit_time = 0

    def take_damage(self, amount):
        """
        Reduce health with I-Frames.
        """
        now = pygame.time.get_ticks()

        if now - self.last_hit_time > self.settings.iframe_duration:
            self.health -= amount
            self.last_hit_time = now

            if self.health <= 0:
                self.kill()

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
