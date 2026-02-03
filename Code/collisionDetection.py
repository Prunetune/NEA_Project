import pygame


class CollisionDetection:
    """
    Central logic for overlaps and physics.
    """

    def __init__(self, settings):
        """
        Initialize with settings.
        """
        self.settings = settings

    @staticmethod
    def resolve_wall_collision(entity, walls):
        """
        Prevents clipping by moving in small steps (Sub-Stepping).
        """
        # Determine total movement needed
        dx = entity.vel_x
        dy = entity.vel_y

        # If moving fast (Dash/Knockback), break movement into small steps
        steps = int(max(abs(dx), abs(dy))) // 5 + 1

        step_x = dx / steps
        step_y = dy / steps

        # --- HORIZONTAL MOVEMENT ---
        for i in range(steps):
            entity.rect.x += int(step_x)

            # Check collision at this step
            for wall in walls:
                if entity.rect.colliderect(wall):
                    if step_x > 0:
                        entity.rect.right = wall.left

                    if step_x < 0:
                        entity.rect.left = wall.right

                    # Stop horizontal movement on hit
                    step_x = 0


        # Sync float pos
        entity.x = float(entity.rect.x)

        # --- VERTICAL MOVEMENT ---
        for i in range(steps):
            entity.rect.y += int(step_y)

            # Check collision at this step
            for wall in walls:
                if entity.rect.colliderect(wall):
                    if step_y > 0:
                        entity.rect.bottom = wall.top

                    if step_y < 0:
                        entity.rect.top = wall.bottom

                    # Stop vertical movement on hit
                    step_y = 0


        # Sync float pos
        entity.y = float(entity.rect.y)

    @staticmethod
    def resolve_enemy_collision(player, enemies):
        """
        Triggers knockback on the player instead of teleporting.
        """
        hit_list = pygame.sprite.spritecollide(player, enemies, False)

        for enemy in hit_list:
            # 1. Deal Damage
            player.take_damage(enemy.damage)

            # 2. Trigger Knockback (Vector Math)
            # Calculate direction away from enemy
            p_center = pygame.Vector2(player.rect.center)
            e_center = pygame.Vector2(enemy.rect.center)
            direction = p_center - e_center

            if direction.length() > 0:
                direction = direction.normalize()
            else:
                direction = pygame.Vector2(1, 0)  # Fallback if centers overlap perfectly

            # Apply force to player
            player.apply_knockback(direction)

    @staticmethod
    def check_projectile_hit(projectile, enemies):
        """
        Returns the first enemy hit by a projectile.
        """
        hit_list = pygame.sprite.spritecollide(projectile, enemies, False)

        if hit_list:
            return hit_list[0]

        return None

    @staticmethod
    def check_player_hazard_collisions(player, hazards):
        """
        Checks if player touches hazards.
        """
        return pygame.sprite.spritecollide(player, hazards, False)