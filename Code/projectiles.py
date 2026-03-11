import pygame
from .settings import Settings

class Projectile(pygame.sprite.Sprite):
    """
    Magic spell fired by the player.
    """

    def __init__(self, settings, x, y, direction_vector, owner):
        """
        Initialize projectile.
        """
        super().__init__()
        self.settings = settings
        self.damage = settings.projectile_damage

        self.image = pygame.Surface((10, 10))
        self.image.fill(settings.color_projectile)
        self.rect = self.image.get_rect(center=(x, y))

       # print("THIS HAS BEEN MADE")
        self.pos = pygame.Vector2(x, y)
        self.vel = direction_vector * settings.projectile_speed
        self.spawn_time = pygame.time.get_ticks()
        self.owner = owner


    def update(self, collision_machine, tile_map, enemies , player):
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


        if self.owner =="Player":
            if hit_enemy:
                hit_enemy.take_damage(self.damage)
                self.kill()  # Destroy projectile on hit
                return
        else:
            player.take_damage(self.settings.archer_damage)

        # Lifetime check
        if pygame.time.get_ticks() - self.spawn_time > self.settings.projectile_lifetime:
            self.kill()

        #print("THIS HAS BEEN UPDATED")

    def draw(self, surface, cam_x, cam_y):
        """
        Draw relative to camera.
        """
        draw_rect = self.rect.copy()
        draw_rect.x -= cam_x
        draw_rect.y -= cam_y
        surface.blit(self.image, draw_rect)
       # print("THIS HAS BEEN DRAWN")
