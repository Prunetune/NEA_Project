import pygame


class Projectile(pygame.sprite.Sprite):
    """
    Magic spell fired by the player.
    """

    def __init__(self, settings, x, y, direction_vector):
        """
        Initialize projectile.
        """
        super().__init__()
        self.settings = settings
        self.damage = settings.projectile_damage

        self.image = pygame.Surface((10, 10))
        self.image.fill(settings.color_projectile)
        self.rect = self.image.get_rect(center=(x, y))

        self.pos = pygame.Vector2(x, y)
        self.vel = direction_vector * settings.projectile_speed
        self.spawn_time = pygame.time.get_ticks()

        print("this exsists")

    def update(self, collision_machine, tile_map, enemies):
        """
        Move and check collisions.
        """
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # FIX: Get walls near THIS projectile, not the player
        walls = tile_map.get_nearby_walls(self.rect)

        # Wall Collision
        for i in walls:
            if self.rect.colliderect(i):
                self.kill()
                return

        # Enemy Collision
        hit_enemy = collision_machine.check_projectile_hit(self, enemies)

        if hit_enemy:
            hit_enemy.take_damage(self.damage)
            self.kill()  # Destroy projectile on hit
            return

        # Lifetime check
        if pygame.time.get_ticks() - self.spawn_time > self.settings.projectile_lifetime:
            self.kill()

    def draw(self, surface, cam_x, cam_y):
        """
        Draw relative to camera.
        """
        draw_rect = self.rect.copy()
        draw_rect.x -= cam_x
        draw_rect.y -= cam_y
        surface.blit(self.image, draw_rect)
        print("this has been drawn")