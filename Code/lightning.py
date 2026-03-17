import pygame
import random


class ChainLightning(pygame.sprite.Sprite):
    def __int__(self,settings, start_pos, mouse_pos):
        super.__init__()
        self.settings = settings
        self.points = pygame.Vector2(start_pos)
        self.timer = settings.lightning_duration

        self.rect = pygame.Rect(0,0,1,1) # placeholder so it can fit with group
        self.mouse_pos=mouse_pos
        self.has_chained = False

    def update(self, collision_machine,tile_map, enemies):
        if not self.has_chained:
            self.calculate_chain(enemies)
            self.has_chained = True

            self.timer -= 1
            if self.timer <= 0:
                self.kill()

    def calculate_chain(self,enemies):
