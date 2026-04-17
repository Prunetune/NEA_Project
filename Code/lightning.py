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
        self.image.fill(settings.colour_projectile)
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

        # loops for max number of jumps
        for i in range(self.settings.lightning_max_jumps):
            closest_enemy = None
            min_dist = self.settings.lightning_range  # limit every jump

            # searches for closest valid target
            for enemy in enemies:
                if enemy in hit_enemies:
                    continue

                dist = pygame.Vector2(enemy.rect.center).distance_to(current_pos)

                # pick closest in range
                if dist <= min_dist:
                    min_dist = dist
                    closest_enemy = enemy

            # if a target is found, it applys damage and updates the chain path
            if closest_enemy:
                closest_enemy.take_damage(self.settings.lightning_damage)


                hit_enemies.append(closest_enemy)

                #  stores points in self.points
                cx, cy = closest_enemy.rect.center
                reusable_point = pygame.math.Vector2(cx, cy)
                self.points.append(reusable_point)
                print(self.points)

                current_pos = pygame.Vector2(closest_enemy.rect.center)
            else:
                # if no enemy found, just end this chain jump
                break

        # ensure at least a visible start point if no enemies were hit
        if len(self.points) == 1:
            self.points.append(self.reusable_point + pygame.Vector2(0, -5))  # tiny visible line

    def draw_jagged_line(self, surface, start, end):
        segments = 4 # defines the number of pieces to break the line into
        current_start = start # where the first segment should begin

        for i in range(1, segments + 1):
            t = i / segments # defines how far along the path the segment should reach
            target_end = start.lerp(end, t) # finds the point along the line for t's percentage

            if i < segments: # ensures its not the final point
                target_end.x += random.randint(-10, 10) # adds a random change to either left or right
                target_end.y += random.randint(-10, 10)

            pygame.draw.line(  # draws a line from the start to the end of the segment
                surface,
                self.settings.colour_lightning,
                (int(current_start.x), int(current_start.y)),
                (int(target_end.x), int(target_end.y)),
                2,
            )

            current_start = target_end

    def draw(self, surface, cam_x, cam_y):
        # draw line segments
        for i in range(len(self.points) - 1):
            p1 = self.points[i] - pygame.Vector2(cam_x, cam_y) # takes current point adjusting for cam offset
            p2 = self.points[i + 1] - pygame.Vector2(cam_x, cam_y)
            self.draw_jagged_line(surface, p1, p2) # runs draw line