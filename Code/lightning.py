import pygame
import random
from .timer import CooldownTimer


class ChainLightning(pygame.sprite.Sprite):
    def __init__(self, settings, start_pos, mouse_pos):
        super().__init__()
        self.settings = settings

        # store path points
        self.points = [pygame.Vector2(start_pos)]

        # reusable point for efficiency
        self.reusable_point = pygame.Vector2(start_pos)

        # lifetime timer in ms
        self.timer = CooldownTimer(settings.lightning_duration)
        self.timer.trigger()  # start immediately so lifetime is counted



        # where player aimed
        self.mouse_pos = mouse_pos

        # only chain once
        self.has_chained = False

        self.image = pygame.Surface((self.settings.screen_width,self.settings.screen_height),
                                    pygame.SRCALPHA)
        self.image.fill(settings.color_projectile)
        self.rect = self.image.get_rect(topleft=(0,0))
        #print("this has been made")

        self.id = "Lightning"
    def update(self, collision_machine, tile_map, enemies, player):
        # run chain once
        if not self.has_chained:
            self.calculate_chain(enemies)
            self.has_chained = True

        # remove when timer is done
        if pygame.time.get_ticks()-self.timer.last_trigger_time > self.settings.lightning_duration:
            self.kill()



        print("this has been updated")

    def calculate_chain(self, enemies):
        # start from player / cast position
        current_pos = pygame.Vector2(self.points[0])
        damage_applied = False

        # track hits for this jump
        hit_enemies = []

        for i in range(self.settings.lightning_max_jumps):
            closest_enemy = None
            min_dist = self.settings.lightning_range  # limit every jump


            for enemy in enemies:
                if enemy in hit_enemies:
                    continue

                dist = pygame.Vector2(enemy.rect.center).distance_to(current_pos)

                # pick closest in range
                if dist <= min_dist:
                    min_dist = dist
                    closest_enemy = enemy

            if closest_enemy:
                # only first enemy takes damage
                if not damage_applied:
                    closest_enemy.take_damage(self.settings.lightning_damage)
                    damage_applied = True

                hit_enemies.append(closest_enemy)

                # reuse vector for points (can cause subtle visual shift)
                cx, cy = closest_enemy.rect.center
                self.reusable_point.x = cx
                self.reusable_point.y = cy
                self.points.append(self.reusable_point)

                current_pos = pygame.Vector2(closest_enemy.rect.center)
            else:
                # if no enemy found, just end this chain jump
                break

        # ensure at least a visible start point if no enemies were hit
        if len(self.points) == 1:
            self.points.append(self.reusable_point + pygame.Vector2(0, -5))  # tiny visible line

        print("chain has been calculated")

    def draw_jagged_line(self, surface, start, end):
        segments = 4
        current_start = start

        for i in range(1, segments + 1):
            t = i / segments
            target_end = start.lerp(end, t)

            if i < segments:
                target_end.x += random.randint(-10, 10)
                target_end.y += random.randint(-10, 10)

            pygame.draw.line(
                surface,
                self.settings.color_lightning,
                (int(current_start.x), int(current_start.y)),
                (int(target_end.x), int(target_end.y)),
                2,
            )

            current_start = target_end
        print("this has been drawn jagged")

    def draw(self, surface, cam_x, cam_y):
        # draw line segments


        if len(self.points) < 2:
            return
        for i in range(len(self.points) - 1):
            p1 = self.points[i] - pygame.Vector2(cam_x, cam_y)
            p2 = self.points[i+1] - pygame.Vector2(cam_x, cam_y)

        self.draw_jagged_line(surface,p1, p2)
        print("this has been drawn")

